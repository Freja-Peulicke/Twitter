/** @type {import('tailwindcss').Config} */

const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  mode: "jit",
  content: ["../views/*.html"],
  theme: {
    extend: {
      colors: {
        'twitter': '#1d9bf0',
        'twitter-dark': '#1a8cd8',
        'dim': '#15202b',
        'dim-border': '#38444d'
      },
      width: {
        '4.5': '1.125rem'
      }
    },
    screens: {
      'xs': '500px',
      ...defaultTheme.screens,
    }
  },
  plugins: [],
}