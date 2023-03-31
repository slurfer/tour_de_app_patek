/* eslint-disable tailwindcss/no-custom-classname */
import clsx from "clsx"
import { motion } from "framer-motion"
import { useState } from "react"
import { useDispatch } from "react-redux"
import { putRequest } from "../src/functions/api/put"
import { removeSingleNote, updateSingleNote } from "../src/store/actions"
import { deleteRequest } from "../src/functions/api/delete"
import { useTranslation } from "react-i18next"
import { SelectColor } from "./formParts"
import { Color } from "../src/types"
import { sntz } from "../src/functions/api"

export const Sticknote = ({ content, author, color, id }: { content: string; author: string, color:any,id:number }) => {

  const [contentState, setContentState] = useState(content)
  const [authorState, setAuthorState] = useState(author)
  const [errorMesage, setErrorMesage] = useState<string>("")  
  const [colorState, setColorState] = useState<Color>(color)
  const dispatch = useDispatch()
  const {t} = useTranslation()
  
  const handleContentChange = (event: any) => {
    setContentState(sntz(event.target.value))
    setErrorMesage(t("Unsaved_data") as string)
  }

  const handleColorChange = (event: any) => {
    setColorState(event.target.value)
    setErrorMesage(t("Unsaved_data") as string)
  }

  const handleAuthorChange = (event: any) => {
    setAuthorState(sntz(event.target.value))
    setErrorMesage(t("Unsaved_data") as string)
  }

  const handleDeleting = () => {
    deleteRequest("note",id)
    dispatch(removeSingleNote(id))
  }

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const newNote = {
      content: contentState,
      author: authorState,
      color: colorState,
      id:3
    }
    putRequest("note",id,newNote)
    console.log("Zvládl jsi to Karlíku")
    dispatch(updateSingleNote(id,newNote))
    console.log(newNote)
    setErrorMesage("")
  }

  const getLighterColor = (colorName:"yellow"|"orange"|"red"|"pink"|"purple"|"blue"|"green"|"brown") =>{
    switch (colorName) {
    case "yellow":
      return("bg-[#fff27f]")
    case "orange":
      return("bg-[#ff9966]")
    case "red":
      return("bg-[#ff6666]")
    case "pink":
      return("bg-[#ff99cc]")
    case "purple":
      return("bg-[#cc99ff]")
    case "blue":
      return("bg-[#99ccff]")
    case "green":
      return("bg-[#99ff99]")
    case "brown":
      return("bg-[#cc9966]")
    default:
      return("bg-[#fff27f]")
    }
  }

  return (
    <motion.form 
      whileHover={{ y: -10 }}
      className={clsx("m-1 h-[250px] w-[19%] p-5",getLighterColor(colorState))}
      onSubmit={handleSubmit}
    >
      <textarea 
        maxLength={20}
        value={authorState} 
        className="mt-2 h-[25px] w-full bg-transparent font-bold"
        onChange={handleAuthorChange}
      />
      <br />
      <textarea 
        maxLength={120}
        className="h-[70px] w-full overflow-scroll bg-transparent" 
        value={contentState} 
        onChange={handleContentChange}
      />
      <p className="h-[25px] text-center font-bold text-[#ff0000]">{errorMesage&&errorMesage}</p>
      <div className="flex w-full">
        <SelectColor text="Choose from eight different colors" value={colorState} onChange={handleColorChange} />
      </div>
      <div className="mt-2 flex">
        <div className="m-auto flex w-fit">
          <motion.img 
            src="/bin.png"
            className="mr-3 h-[25px] cursor-pointer"
            onClick={handleDeleting}
            whileHover={{ scale:1.5 }}
          />
          <button className="m-auto" type="submit">
            <motion.img 
              whileHover={{ scale:1.5 }}
              src="/tick.png"
            />
          </button>
        </div>
      </div>
    </motion.form>
  )
}