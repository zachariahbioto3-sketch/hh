/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        forest: '#1B1A4F',
        leaf: '#8080B8',
        gold: '#AEAED0',
        charcoal: '#1B1A4F',
        navy: '#1B1A4F',
        purple: '#8080B8',
        lavender: '#AEAED0'
      },
      fontFamily: {
        display: ['"Playfair Display"', 'serif'],
        body: ['Inter', 'sans-serif']
      }
    }
  },
  plugins: [],
}
