// tailwind.config.js
module.exports = {
  darkMode: 'class', // Esto es esencial para el modo oscuro manual
  content: [
    './templates/**/*.html',
    // Añade aquí otros paths donde uses clases de Tailwind
  ],
  theme: {
    extend: {
      // Tus extensiones personalizadas
    },
  },
  plugins: [
    // Tus plugins
  ],
}