/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        earth: {
          50: "#f7f4ef",
          100: "#ebe4d6",
          700: "#3f5c3a",
          800: "#2c4a3a",
          900: "#1c3328",
        },
        clay: "#c46a3a",
      },
    },
  },
  plugins: [],
};
