/** @type {import('tailwindcss').Config} */
module.exports = {
  mode:"jit",
  content: ["../views/*.html"],
  theme: {
    extend: {
      colors: {
        twitter: "#1d9bf0",
        grey: "#0f1419"
      }
    },
  },
  plugins: [],
}
