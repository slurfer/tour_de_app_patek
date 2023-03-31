/* eslint-disable jsx-a11y/alt-text */
/* eslint-disable @next/next/no-img-element */

import { useState } from "react"
import { useRouter } from "next/router"
import clsx from "clsx"
import { useSelector } from "react-redux"
import { motion } from "framer-motion"
import { State } from "../../src/types"
import { SideBarLink } from "./SideBarLink"

export const Sidebar = ({ hidden }: { hidden?: boolean }) => {
  const router = useRouter()
  const { mode } = useSelector((state: State) => state)
  const [isOpen, setIsOpen] = useState<boolean>(false)
  const variants = {
    open: { opacity: 1, y: 0 },
    closed: { opacity: 0, y: "-50%" },
  }

  return (
    <div 
      className={clsx("w-[20%]",hidden&&"hidden md:block")}
    >
      <motion.img
        whileHover={{ scale:1.2 }}
        className="h-[40px] min-w-[40px] cursor-pointer"
        src={mode ? "otevrit_stranku_bila.png" : "otevrit_stranku.png"}
        onClick={() => setIsOpen(true)}
      />
      <div
        className={`
      ${isOpen ? "w-[350px] p-20" : "w-0"} ${
      mode ? isOpen && "border border-white bg-main_color" : "bg-light_blue"
    } fixed left-0 top-0 z-10 h-full text-white duration-300`}
      >
        <motion.div 
          animate={isOpen ? "open" : "closed"}
          variants={variants}
          transition={{ duration: 0.5 }}
          className={` ${isOpen?"block":"hidden"} text-2xl`}>
          <img className="relative bottom-[60px] left-[200px] w-[50px] cursor-pointer" src={"zavrit_stranku.png"} onClick={()=>setIsOpen(false)}/>
          <SideBarLink page={router.pathname} text="Home" href="/" />
          <br />
          <br />
          <SideBarLink page={router.pathname} text="Statistics" href="/statistics" />
          <br />
          <br />
          <SideBarLink page={router.pathname} text="Information" href="/information" />
        </motion.div>
      </div>
    </div>
  )
}
