import { Page } from "../components/Page"
import { Header } from "../components/Header"
import { ResponsiveText } from "../components/ReponsiveText"
import { useTranslation } from "react-i18next"

export default function AboutUs () {

  const { t } = useTranslation()

  return (
    <Page>
      <title>Sticknotes | Information</title>
      <Header />
      <ResponsiveText className="text-center">{t("About_us")}</ResponsiveText>
    </Page>
  )
}