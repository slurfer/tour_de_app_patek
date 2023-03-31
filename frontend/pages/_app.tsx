import "../styles/globals.css"
import NextNProgress from "nextjs-progressbar"
import type { AppProps } from "next/app"
import { Provider } from "react-redux"
import { store, wrapper } from "../src/store/store"
import { I18nextProvider } from "react-i18next"
import i18n from "../i18n"

function App({ Component, pageProps }: AppProps) {
  return (
    <I18nextProvider i18n={i18n}>
      <Provider store={store}>
        <NextNProgress />
        <Component {...pageProps} />:
      </Provider>
    </I18nextProvider>
  )
}

export default wrapper.withRedux(App)
