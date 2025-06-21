// theme/static_src/tailwind.config.js
module.exports = {
  content: [
    '../../templates/**/*.{html,js}', // ✅ Esto es crucial para que Tailwind escanee tus plantillas HTML
    // Agrega aquí cualquier otra ruta donde uses clases de Tailwind, por ejemplo:
    // '../**/templates/**/*.{html,js}', // Si tienes plantillas dentro de otras apps en 'applications/'
    // './src/**/*.js', // Si tienes archivos JS en src/ que añaden clases de Tailwind
  ],
  darkMode: 'class',
  theme: {
    extend: {},
  },
  plugins: [],
}