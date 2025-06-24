/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../../templates/**/*.{html,js}', // Crucial para que Tailwind escanee tus plantillas HTML
    // Agrega aquí cualquier otra ruta donde uses clases de Tailwind
  ],
  darkMode: 'class', // Habilita el modo oscuro basado en la clase 'dark' en el elemento html
  theme: {
    extend: {
      colors: {
        // --- Paleta "Frozen Elsa" (para un posible modo claro o acentos suaves) ---
        'elsa-purple-dark': '#7B68EE',      // MediumSlateBlue
        'elsa-purple-medium': '#9370DB',    // MediumPurple
        'elsa-purple-light': '#B0C4DE',     // LightSteelBlue
        'elsa-blue-medium': '#87CEEB',      // SkyBlue
        'elsa-blue-light': '#ADD8E6',       // LightBlue
        'elsa-white': '#F0F8FF',            // AliceBlue

        // --- Paleta para el Dashboard Oscuro (Colores principales) ---
        'dark-app-bg': '#1E2024',           // Fondo principal muy oscuro del dashboard
        'dark-card-bg': '#2D3035',          // Fondo de los paneles/cards
        'dark-sidebar-bg': '#2D3035',       // Fondo del sidebar (similar a las cards)
        'dark-header-bg': '#2D3035',        // Fondo del header (similar a las cards)

        // --- Colores de texto e iconos para el dashboard oscuro ---
        'dark-text-primary': '#E0E0E0',     // Texto principal claro
        'dark-text-secondary': '#A0A0A0',   // Texto secundario (etiquetas, subtítulos)
        'dark-icon-color': '#E0E0E0',       // Color de los iconos principales

        // --- Colores de acento para gráficos y elementos interactivos del dashboard ---
        'dashboard-accent-purple': '#7E48E8', // Púrpura vibrante para acentos y gráficos
        'dashboard-accent-cyan': '#4ACADF',   // Azul cian para acentos y gráficos
        'dashboard-progress-green': '#4CAF50', // Verde para barras de progreso, etc.
        'dashboard-progress-red': '#EF5350',   // Rojo para indicar problemas
        
        // --- Bordes y sombras sutiles para el dashboard oscuro ---
        'dark-border-subtle': '#3A3D42',    // Bordes muy oscuros para separación
      },
      boxShadow: {
        'dark-card-shadow': '0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.1)', // Sombra para cards
      }
    },
  },
  plugins: [],
}