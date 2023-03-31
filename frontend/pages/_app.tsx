import "../styles/globals.css"
import NextNProgress from "nextjs-progressbar"
import type { AppProps } from "next/app"
import { Provider } from "react-redux"
import { store, wrapper } from "../src/store/store"
import { I18nextProvider } from "react-i18next"
import i18n from "../i18n"
import { useEffect } from "react"
import { useRouter } from "next/router"

function App({ Component, pageProps }: AppProps) {

  const router = useRouter()
  useEffect(() => {
    const timer = setTimeout(() => {
      router.push("/")
    }, 120000)

    return () => clearTimeout(timer)
  }, [router])

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
