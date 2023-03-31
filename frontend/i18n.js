import i18n from "i18next"
import { initReactI18next } from "react-i18next"

import en from "public/locales/en/translation.json"
import cs from "public/locales/cs/translation.json"

i18n.use(initReactI18next).init({
  lng: "en",
  fallbackLng: "en",
  resources: {
    en: { translation: en },
    cs: { translation: cs }
  },
  interpolation: { escapeValue: false }
})

export default i18n