import { useEffect } from "react"
import { useDispatch, useSelector } from "react-redux"
import { Header } from "../components/Header"
import { Page } from "../components/Page"
import { Sticknotes } from "../components/Sticknotes"
import { getRequest } from "../src/functions/api/get"
import { setNotes } from "../src/store/actions"

export default function Home() {

  const dispatch = useDispatch()
  const notes = useSelector((state:any) => state.notes)
  //const { t } = useTranslation()

  useEffect( () => {
    const updateNotes = async () => {
      const data = await getRequest("note")
      dispatch(setNotes(data))
      console.log("Jedeme bomby:",data)
    }
    updateNotes()
  }, [dispatch])

  return (
    <Page>
      <title>Sticknotes | Homepage</title>
      <Header />
      <Sticknotes data={notes}/>
    </Page>
  )
}
