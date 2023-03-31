import { useState } from "react"
import { postRequest } from "../src/functions/api/post"
import { SelectColor } from "./formParts"
import clsx from "clsx"
import { Color } from "../src/types"
import { addSingleNote } from "../src/store/actions"
import { useDispatch } from "react-redux"
import { useTranslation } from "react-i18next"
import { motion } from "framer-motion"
import { sntz } from "../src/functions/api"

export const NewNote = () => {

  const [contentState, setContentState] = useState<string>("")
  const [authorState, setAuthorState] = useState<string>("")
  const [colorState, setColorState] = useState<Color>("yellow")
  const {t} = useTranslation()
  const dispatch = useDispatch()

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

  const handleContentChange = (event: any) => {
    setContentState(sntz(event.target.value))
  }
    
  const handleAuthorChange = (event: any) => {
    setAuthorState(sntz(event.target.value))
  }

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const newNote = {
      content: contentState,
      author: authorState,
      color: colorState,
      id:3
    }
    postRequest("note",newNote)
    console.log("Zvládl jsi to Karlíku")
    dispatch(addSingleNote(newNote))
    console.log(newNote)
    setContentState(""),setAuthorState(""),setColorState("yellow")
  }

  return (
    <motion.form 
      whileHover={{ y: -10 }}
      onSubmit={handleSubmit} 
      className={clsx("m-1 h-[250px] w-[19%] p-5",getLighterColor(colorState))}
    >
      <textarea 
        maxLength={20}
        required
        className="mt-2 h-[25px] w-full bg-transparent font-bold"
        placeholder={t("Add_user") as string}
        onChange={handleAuthorChange}
        value={authorState}
      />
      <br/>
      <textarea 
        maxLength={120}
        required
        placeholder={t("Add_content") as string}
        className="h-[100px] w-full overflow-scroll rounded-md bg-transparent" 
        onChange={handleContentChange}
        value={contentState}
      />  
      <div className="flex w-full">
        <SelectColor text="Choose from eight different colors" value={colorState} onChange={(event:any)=>{setColorState(event.target.value)}} />
      </div>
      <div className="mt-2 flex w-full rounded-md">
        <button className="m-auto" type="submit">
          <motion.img 
            whileHover={{ scale:1.5 }}
            src="/tick.png"
          />
        </button>
      </div>
    </motion.form>)
}