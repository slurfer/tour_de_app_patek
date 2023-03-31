import { useTranslation } from "react-i18next"
import { Header } from "../components/Header"
import { Page } from "../components/Page"
import { ResponsiveText } from "../components/ReponsiveText"


export default function Home() {

  const { t } = useTranslation()

  return (
    <Page>
      <title>CHANGE IT | Homepage</title>
      <Header />
      <ResponsiveText>
        {t("Introduction")}
      </ResponsiveText>
    </Page>
  )
}
