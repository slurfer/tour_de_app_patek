/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./pages/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        button_green: "rgb(16 185 129)",
        button_red: "rgb(225 29 72)",
        light_blue: "#0018DA",
        entry_color: "#182A46",
        main_color: "#0B182F",
        black: "#000000"
      },
      maxWidth: {
        page_max: "1434px"
      }
    }
  },
  plugins: []
}
