#!/usr/bin/env python3
"""Cross-platform BhuStack bootstrap and local service CLI."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import platform
import re
import shutil
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
FRONTEND = ROOT / "frontend"
DATABASE = ROOT / "database"
RUN = ROOT / ".run"
LOGS = ROOT / "logs"
POSTGIS = "bhustack-postgis"
VENV_DIR = ".venv"
DOCKER_WINDOWS_NAME = "docker.exe"
API_URL = "http://127.0.0.1:8000/api/v1/health"
WEB_URL = "http://127.0.0.1:5173"
CANONICAL_IND_DEMO_COUNT = 30
ADMINISTRATIVE_DEMO_ULPINS = ("1234-5678-9012", "9876-5432-1098")
EXPECTED_TOTAL_PARCELS = CANONICAL_IND_DEMO_COUNT + len(ADMINISTRATIVE_DEMO_ULPINS)
REQUIRED_TABLES = (
    "parcels", "ownership", "ror", "registrations", "land_use", "tax",
    "restrictions", "disputes", "building_permissions", "service_requests",
    "users", "audit_logs", "administrative_regions",
)
DEPARTMENT_TABLES = (
    "ownership", "ror", "registrations", "land_use", "tax",
    "restrictions", "disputes", "building_permissions",
)


def say(message: str) -> None:
    print(f"[BhuStack] {message}", flush=True)


def fail(message: str) -> None:
    raise RuntimeError(message)


def resolve_command(name: str, windows_name: str | None = None) -> str:
    candidates = (windows_name, name) if os.name == "nt" and windows_name else (name,)
    value = next((shutil.which(candidate) for candidate in candidates if candidate), None)
    if not value:
        fail(f"{name} was not found. Install the documented prerequisite and retry.")
    return value


def node_command() -> str:
    return resolve_command("node", "node.exe")


def npm_command() -> str:
    return resolve_command("npm", "npm.cmd")


def docker_command() -> str:
    return resolve_command("docker", DOCKER_WINDOWS_NAME)


def run(args: list[str], *, cwd: Path = ROOT, input_text: str | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, input=input_text, text=True, capture_output=True, check=check)


def print_command_error(label: str, error: subprocess.CalledProcessError) -> None:
    detail = (error.stderr or error.stdout or "No diagnostic was returned.").strip()
    fail(f"{label} failed.\n{detail}")


def backend_python() -> Path:
    return BACKEND / VENV_DIR / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def python_version(candidate: list[str]) -> tuple[int, int, int, str] | None:
    result = subprocess.run(candidate + ["--version"], cwd=ROOT, text=True, capture_output=True, check=False)
    output = (result.stdout or result.stderr).strip()
    match = re.search(r"Python (\d+)\.(\d+)\.(\d+)([^\s]*)", output)
    if result.returncode != 0 or not match:
        return None
    return int(match.group(1)), int(match.group(2)), int(match.group(3)), match.group(4)


def stable_python(candidate: list[str]) -> bool:
    version = python_version(candidate)
    return bool(version and version[:2] >= (3, 10) and not re.search(r"(?:a|b|rc)\d*$", version[3]))


def discover_python() -> list[str]:
    candidates: list[list[str]] = []
    if os.name == "nt" and shutil.which("py"):
        candidates.extend((["py", "-3.12"], ["py", "-3.13"], ["py", "-3"]))
    candidates.extend((["python3.12"], ["python3.13"], ["python3"], ["python"]))
    for candidate in candidates:
        if (candidate[0] == "py" or shutil.which(candidate[0])) and stable_python(candidate):
            return candidate
    fail("No stable Python 3.10+ interpreter was found. Install Python 3.12 and retry.")


def selected_python() -> list[str]:
    return discover_python()


def ensure_python_venv() -> Path:
    p = backend_python()
    if p.exists() and not stable_python([str(p)]):
        say("Replacing backend virtual environment created with an unsupported Python prerelease...")
        shutil.rmtree(BACKEND / VENV_DIR)
    if not p.exists():
        interpreter = selected_python()
        version = python_version(interpreter)
        say(f"Creating backend virtual environment with Python {version[0]}.{version[1]}.{version[2]}...")
        run(interpreter + ["-m", "venv", str(BACKEND / VENV_DIR)])
    return p


def check_prerequisites() -> None:
    selected_python()
    node = node_command()
    npm_command()
    node_version = run([node, "--version"]).stdout.strip().lstrip("v").split(".")[0]
    if not node_version.isdigit() or int(node_version) < 18:
        fail("Node.js 18 or newer is required.")
    docker = docker_command()
    try:
        run([docker, "info"], check=True)
        run([docker, "compose", "version"], check=True)
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or error.stdout or "").lower()
        if "daemon" in detail or "cannot connect" in detail or "not running" in detail:
            fail("Docker is installed but the Docker daemon is not running. Start Docker Desktop/Engine and retry.")
        fail(f"Docker is available but not usable on this machine. Details:\n{detail or error}")


def ensure_envs() -> None:
    for directory in (BACKEND, FRONTEND):
        target, example = directory / ".env", directory / ".env.example"
        if not target.exists() and example.exists():
            target.write_text(example.read_text(encoding="utf-8"), encoding="utf-8")
            say(f"Created {target.relative_to(ROOT)} from its template.")


def docker_compose_up() -> None:
    try:
        run([docker_command(), "compose", "up", "-d", "postgis"])
    except subprocess.CalledProcessError as error:
        print_command_error("PostGIS startup", error)


def wait_postgis(seconds: int = 60) -> None:
    for _ in range(seconds):
        result = run([docker_command(), "exec", POSTGIS, "pg_isready", "-U", "postgres", "-d", "bhustack"], check=False)
        if result.returncode == 0:
            say("PostGIS ready.")
            return
        time.sleep(1)
    fail("PostGIS did not become ready within 60 seconds. Run `docker compose logs postgis` for details.")


def psql(sql: str | None = None, file: Path | None = None) -> str:
    content = file.read_text(encoding="utf-8") if file else sql
    result = run([docker_command(), "exec", "-i", POSTGIS, "psql", "-tA", "-v", "ON_ERROR_STOP=1", "-U", "postgres", "-d", "bhustack"], input_text=content)
    return result.stdout


def verify_database() -> None:
    required_tables = ",".join(f"'{table}'" for table in REQUIRED_TABLES)
    department_counts = ",".join(f"(SELECT COUNT(*) FROM {table})" for table in DEPARTMENT_TABLES)
    query = f"""
SELECT
    (SELECT COUNT(*) FROM parcels WHERE ulpin LIKE 'IND-DEMO-%'),
    (SELECT COUNT(*) FROM parcels WHERE ulpin IN ('1234-5678-9012', '9876-5432-1098')),
    (SELECT COUNT(*) FROM parcels),
    (SELECT COUNT(DISTINCT ulpin) FROM parcels),
    (SELECT COUNT(*) FROM (SELECT ulpin FROM parcels GROUP BY ulpin HAVING COUNT(*) > 1) duplicates),
    (SELECT COUNT(*) FROM ownership),
    (SELECT COUNT(*) FROM pg_extension WHERE extname = 'postgis'),
    (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name IN ({required_tables})),
    (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'administrative_regions'),
    (SELECT LEAST({department_counts}));
"""
    values = [int(part.strip()) for part in psql(query).split("|")]
    canonical, administrative, total, distinct, duplicates, ownership, postgis, tables, admin_regions, departments = values
    say("Database verification:")
    say("  PostgreSQL: OK")
    say(f"  PostGIS: {'OK' if postgis == 1 else 'FAIL'}")
    say(f"  parcels table: {'OK' if tables == len(REQUIRED_TABLES) else 'FAIL'}")
    say(f"  IND-DEMO parcels: {canonical}/{CANONICAL_IND_DEMO_COUNT}")
    say(f"  administrative demo parcels: {administrative}/{len(ADMINISTRATIVE_DEMO_ULPINS)}")
    say(f"  total parcels: {total}/{EXPECTED_TOTAL_PARCELS}")
    say(f"  duplicate ULPINs: {duplicates}")
    say(f"  ownership records: {ownership}/{EXPECTED_TOTAL_PARCELS}")
    say(f"  required department tables: {'OK' if tables == len(REQUIRED_TABLES) and admin_regions == 1 else 'FAIL'}")
    say(f"  department records: {'OK' if departments == EXPECTED_TOTAL_PARCELS else 'FAIL'}")
    valid = (
        canonical == CANONICAL_IND_DEMO_COUNT and administrative == len(ADMINISTRATIVE_DEMO_ULPINS)
        and total == EXPECTED_TOTAL_PARCELS and distinct == EXPECTED_TOTAL_PARCELS and duplicates == 0
        and ownership == EXPECTED_TOTAL_PARCELS and postgis == 1 and tables == len(REQUIRED_TABLES)
        and admin_regions == 1 and departments == EXPECTED_TOTAL_PARCELS
    )
    if not valid:
        fail("Database verification failed. Review the explicit counts above; no data was deleted.")
    say("  Result: PASS")


def db_init() -> None:
    say("Applying database schema...")
    psql(file=DATABASE / "schema.sql")
    parcel_count = int(psql("SELECT COUNT(*) FROM parcels;").strip())
    if parcel_count == 0:
        existing_rows = psql(
            """
            SELECT EXISTS (SELECT 1 FROM ownership)
                OR EXISTS (SELECT 1 FROM ror)
                OR EXISTS (SELECT 1 FROM registrations)
                OR EXISTS (SELECT 1 FROM land_use)
                OR EXISTS (SELECT 1 FROM tax)
                OR EXISTS (SELECT 1 FROM restrictions)
                OR EXISTS (SELECT 1 FROM disputes)
                OR EXISTS (SELECT 1 FROM building_permissions)
                OR EXISTS (SELECT 1 FROM service_requests)
                OR EXISTS (SELECT 1 FROM users)
                OR EXISTS (SELECT 1 FROM audit_logs);
            """
        ).strip().lower() == "t"
        if existing_rows:
            fail("Database is inconsistent: parcels is empty but other application tables contain data. Use db-reset --yes only for a deliberate synthetic reset.")
        say("Loading deterministic canonical seed data...")
        psql(file=DATABASE / "seed.sql")
    else:
        say(f"Reusing existing database with {parcel_count} parcel records; seed data will not be truncated.")
    say("Running idempotent administrative data ingestion...")
    run([str(ensure_python_venv()), str(ROOT / "scripts" / "ingest_administrative_data.py")], cwd=ROOT)
    verify_database()


def ensure_dependencies() -> None:
    python = ensure_python_venv()
    say("Installing backend dependencies...")
    try:
        run([str(python), "-m", "pip", "install", "--upgrade", "pip"], cwd=BACKEND)
        run([str(python), "-m", "pip", "install", "-r", "requirements.txt"], cwd=BACKEND)
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or error.stdout or "").lower()
        if any(word in detail for word in ("temporary failure", "name or service", "connection", "network")):
            fail("Python dependencies could not be downloaded. Check your internet/DNS connection and retry.\n" + (error.stderr or error.stdout))
        print_command_error("Python dependency installation", error)
    say("Installing frontend dependencies...")
    npm = npm_command()
    npm_install = [npm, "ci"] if (FRONTEND / "package-lock.json").exists() else [npm, "install"]
    try:
        run(npm_install, cwd=FRONTEND)
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or error.stdout or "").lower()
        if any(word in detail for word in ("enotfound", "network", "registry", "dns")):
            fail("npm dependencies could not be downloaded. Check your internet/DNS connection and retry.\n" + (error.stderr or error.stdout))
        print_command_error("npm dependency installation", error)


def require_initialized() -> None:
    python = backend_python()
    if not python.exists() or not (FRONTEND / "node_modules").exists():
        fail("Project dependencies are not initialized. Run `python scripts/init.py` first.")


def http_ready(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            return 200 <= response.status < 300
    except (urllib.error.URLError, TimeoutError):
        return False


def api_ready() -> bool:
    try:
        with urllib.request.urlopen(API_URL, timeout=2) as response:
            return response.status == 200 and json.loads(response.read()).get("status") == "ok"
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return False


def state_file(name: str) -> Path:
    RUN.mkdir(exist_ok=True)
    return RUN / f"{name}.json"


def pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def read_state(name: str) -> dict | None:
    path = state_file(name)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
        if pid_alive(int(data["pid"])):
            return data
    except (ValueError, KeyError):
        pass
    path.unlink(missing_ok=True)
    return None


def process_args(name: str) -> tuple[list[str], Path]:
    python = backend_python()
    if name == "backend":
        return ([str(python), "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"], BACKEND)
    return ([npm_command(), "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"], FRONTEND)


def start_service(name: str, url: str) -> None:
    existing = read_state(name)
    ready = api_ready() if name == "backend" else http_ready(url)
    if existing and ready:
        say(f"{name.capitalize()} already running.")
        return
    if existing:
        say(f"Restarting unhealthy managed {name}...")
        stop_service(name)
    args, cwd = process_args(name)
    LOGS.mkdir(exist_ok=True)
    log = (LOGS / f"{name}.log").open("a", encoding="utf-8")
    say(f"Starting {name}...")
    kwargs: dict = {"cwd": cwd, "stdout": log, "stderr": subprocess.STDOUT}
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        kwargs["start_new_session"] = True
    process = subprocess.Popen(args, **kwargs)
    state_file(name).write_text(json.dumps({"pid": process.pid, "started": time.time()}), encoding="utf-8")
    say(f"Waiting for {name}...")
    for _ in range(45):
        if (api_ready() if name == "backend" else http_ready(url)):
            say(f"{name.capitalize()} ready.")
            return
        if process.poll() is not None:
            break
        time.sleep(1)
    recent = (LOGS / f"{name}.log").read_text(encoding="utf-8", errors="replace")[-4000:]
    state_file(name).unlink(missing_ok=True)
    fail(f"{name.capitalize()} failed to start. Recent log output:\n{recent}")


def stop_service(name: str) -> None:
    state = read_state(name)
    if not state:
        say(f"No managed {name} process.")
        return
    pid = int(state["pid"])
    say(f"Stopping {name} (PID {pid})...")
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], check=False, capture_output=True)
        else:
            os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    for _ in range(10):
        if not pid_alive(pid):
            break
        time.sleep(1)
    if pid_alive(pid) and os.name != "nt":
        os.killpg(pid, signal.SIGKILL)
    state_file(name).unlink(missing_ok=True)
    say(f"{name} stopped.")


def doctor(_: argparse.Namespace) -> None:
    issues: list[str] = []
    issues.extend(check_python())
    issues.extend(check_node_npm())
    issues.extend(check_docker())
    if not backend_python().exists():
        issues.append("Backend Python virtual environment is not initialized.")
    if not (FRONTEND / "node_modules").exists():
        issues.append("Frontend dependencies are not installed.")
    if not (BACKEND / ".env").exists():
        issues.append("Backend .env file is missing.")
    if not (FRONTEND / ".env").exists():
        issues.append("Frontend .env file is missing.")
    issues.extend(check_database_health())
    if issues:
        say("Doctor found issues:")
        for issue in issues:
            say(f" - {issue}")
        sys.exit(1)
    say("Doctor checks passed: dependencies, environment files, and Docker availability look good.")


def check_python() -> list[str]:
    try:
        interpreter = selected_python()
        version = python_version(interpreter)
        say(f"Selected Python: {' '.join(interpreter)} ({version[0]}.{version[1]}.{version[2]})")
        return []
    except RuntimeError as error:
        return [str(error)]


def check_node_npm() -> list[str]:
    issues: list[str] = []
    if not shutil.which("node"):
        return ["Node.js is not installed."]
    node = node_command()
    version = run([node, "--version"], check=False).stdout.strip().lstrip("v")
    if not version or not version[0].isdigit() or int(version.split(".")[0]) < 18:
        issues.append("Node.js version must be 18 or newer.")
    try:
        npm = npm_command()
        say(f"Resolved npm: {npm}")
        if run([npm, "--version"], check=False).returncode != 0:
            issues.append("npm is not executable.")
    except RuntimeError as error:
        issues.append(str(error))
    return issues


def check_docker() -> list[str]:
    try:
        docker = docker_command()
    except RuntimeError as error:
        return [str(error)]
    if run([docker, "info"], check=False).returncode != 0:
        return ["Docker daemon is not running."]
    if run([docker, "compose", "version"], check=False).returncode != 0:
        return ["Docker Compose is unavailable."]
    return []


def check_database_health() -> list[str]:
    try:
        docker = docker_command()
        if run([docker, "exec", POSTGIS, "pg_isready", "-U", "postgres", "-d", "bhustack"], check=False).returncode != 0:
            return ["PostGIS container is not ready."]
        verify_database()
    except RuntimeError as error:
        return [str(error)]
    return []


def init(_: argparse.Namespace) -> None:
    interpreter = selected_python()
    version = python_version(interpreter)
    say(f"Initializing on {platform.system()} with Python {version[0]}.{version[1]}.{version[2]}...")
    check_prerequisites(); ensure_envs(); ensure_dependencies(); docker_compose_up(); wait_postgis(); db_init()
    backend_was_running = bool(read_state("backend") and api_ready())
    start_service("backend", API_URL)
    try:
        test(argparse.Namespace())
    finally:
        if not backend_was_running:
            stop_service("backend")
    say("Validating frontend build...")
    run([npm_command(), "run", "build"], cwd=FRONTEND)
    say("Initialization complete. Start with: python scripts/start.py")


def start(_: argparse.Namespace) -> None:
    check_prerequisites(); require_initialized(); ensure_envs(); docker_compose_up(); wait_postgis(); verify_database()
    start_service("backend", API_URL); start_service("frontend", WEB_URL)
    say("Opening browser...")
    try:
        webbrowser.open("http://localhost:5173", new=2)
    except Exception:
        pass
    say("Ready: http://localhost:5173 (API docs: http://localhost:8000/docs)")


def stop(_: argparse.Namespace) -> None:
    stop_service("frontend"); stop_service("backend")
    if shutil.which("docker") or (os.name == "nt" and shutil.which(DOCKER_WINDOWS_NAME)):
        subprocess.run([docker_command(), "compose", "stop", "postgis"], cwd=ROOT, check=False)
    say("Stopped. PostGIS data is preserved.")


def db_reset(args: argparse.Namespace) -> None:
    if not args.yes:
        fail("db-reset is destructive and removes the Docker PostGIS volume. Re-run with `db-reset --yes` to confirm.")
    say("WARNING: deleting the synthetic BhuStack PostGIS volume and recreating all demo data.")
    run([docker_command(), "compose", "down", "-v"], cwd=ROOT)
    docker_compose_up()
    wait_postgis()
    db_init()


def test(_: argparse.Namespace) -> None:
    verify_database()
    if not api_ready():
        fail("Backend is not healthy. Run `python scripts/start.py` first.")
    python = backend_python()
    run([str(python), "tests/smoke_api.py"], cwd=BACKEND)
    say("Smoke test passed.")


def status(_: argparse.Namespace) -> None:
    if not (shutil.which("docker") or (os.name == "nt" and shutil.which(DOCKER_WINDOWS_NAME))):
        say("PostGIS: unavailable (docker not installed)")
    else:
        result = run([docker_command(), "exec", POSTGIS, "pg_isready", "-U", "postgres", "-d", "bhustack"], check=False)
        say(f"PostGIS: {'ready' if result.returncode == 0 else 'not ready'}")
    say(f"Backend: {'ready' if api_ready() else 'not ready'}")
    say(f"Frontend: {'ready' if http_ready(WEB_URL) else 'not ready'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="BhuStack cross-platform project CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, handler in (
        ("init", init),
        ("start", start),
        ("stop", stop),
        ("test", test),
        ("status", status),
        ("doctor", doctor),
        ("db-init", lambda _: db_init()),
        ("db-reset", db_reset),
    ):
        command_parser = sub.add_parser(name)
        if name == "db-reset":
            command_parser.add_argument("--yes", action="store_true", help="confirm destructive synthetic database reset")
        command_parser.set_defaults(handler=handler)
    try:
        args = parser.parse_args()
        result = args.handler(args)
        if result is not None and isinstance(result, int):
            raise SystemExit(result)
    except RuntimeError as error:
        say(f"ERROR: {error}")
        raise SystemExit(1)
    except subprocess.CalledProcessError as error:
        detail = error.stderr or error.stdout or ""
        say(f"ERROR: Command failed: {' '.join(error.cmd)}\n{detail}")
        raise SystemExit(error.returncode or 1)


if __name__ == "__main__":
    main()
