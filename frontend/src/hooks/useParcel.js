import { useCallback, useState } from "react";
import { api } from "../services/api";

export function useParcel() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const load = useCallback(async (ulpin) => {
    if (!ulpin) return null;
    setLoading(true);
    setError("");
    try {
      const data = await api.parcel(ulpin);
      setProfile(data);
      return data;
    } catch (err) {
      setProfile(null);
      setError(err.message);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  return { profile, loading, error, load, setProfile };
}
