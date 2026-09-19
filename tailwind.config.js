/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#522888',
          dark: '#3b1a6b',
          light: '#7c4dbb',
        },
        accent: '#ffffff',
        dark: '#0b0b0b',
        muted: '#6b7280',
        card: '#f9f9f9',
        border: '#e5e7eb',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}