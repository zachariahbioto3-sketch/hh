/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          purple: '#522888',
          'purple-dark': '#3b1a6b',
          'purple-light': '#7c4dbb',
          'purple-muted': '#f3eefa',
          black: '#0b0b0b',
          dark: '#0f172a',
          light: '#f8fafc',
          border: '#e2e8f0',
        }
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Inter', 'sans-serif'],
      },
      boxShadow: {
        'card': '0 10px 30px -5px rgba(0, 0, 0, 0.05)',
        'hover': '0 20px 35px -10px rgba(0, 0, 0, 0.12)',
        'glow': '0 0 25px rgba(82, 40, 136, 0.35)',
      }
    }
  },
  plugins: [],
}