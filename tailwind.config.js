/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './website/templates/**/*.html',
    './website/static/**/*.js',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'primary': '#00ff9d',
        'primary-hover': '#00e089',
        'darker-bg': '#121212',
        'card-bg': '#1a1a1a',
      },
      backgroundColor: {
        'darker-bg': '#121212',
        'card-bg': '#1a1a1a',
      },
    },
  },
  plugins: [],
}
