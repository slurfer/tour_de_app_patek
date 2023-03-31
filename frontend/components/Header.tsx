import clsx from "clsx"
import { useDispatch, useSelector } from "react-redux"

import { toggleMode } from "../src/store/actions"
import { Sidebar } from "./sidebar/Sidebar"
import { motion } from "framer-motion"
import { useTranslation } from "react-i18next"

/* eslint-disable jsx-a11y/alt-text */
/* eslint-disable @next/next/no-img-element */

export const Header = () => {
  const dispatch = useDispatch()
  const mode = useSelector((state: any) => state.mode)
  const { i18n } = useTranslation()

  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng)
  }

  return (
    <div>
      <div className="m-auto mb-10 hidden w-[92%] md:flex">
        {" "}
        {/*VISIBLE ON COMPUTER*/}
        <div className="w-[20%] pt-[2px]">
          <Sidebar hidden />
        </div>
        <div className={clsx("w-[60%] text-center text-5xl font-bold", mode ? "text-white " : "")}>
          <p className="m-auto flex w-fit">
            Stick<span className={!mode ? "text-light_blue hover:opacity-80" : "text-white"}>&nbsp;notes.</span>
          </p>
        </div>
        <div className="flex w-[20%] justify-end">
          <motion.img
            whileHover={{ scale:1.2 }}
            className="my-auto mr-8 h-[45px] cursor-pointer"
            src={i18n.language =="en" ? "cs.png" : "en.png"}
            onClick={() => changeLanguage(i18n.language =="cs" ? "en" : "cs")}
          />        
          <motion.img
            whileHover={{ scale:1.2 }}
            className="my-auto h-[40px] w-[40px] cursor-pointer"
            src={mode ? "zmena_modu_bila.png" : "zmena_modu.png"}
            onClick={() => dispatch(toggleMode())}
          />
        </div>
      </div>

      <>
        <div className="m-auto flex w-full md:hidden">
          {" "}
          {/*VISIBLE ON PHONE*/}
          <div className="w-[50%]">
            <Sidebar />
          </div>
          <div className="flex w-[50%] justify-end">
            <img className="mr-2 h-[40px] cursor-pointer" src={i18n.language =="en" ? "cs.png" : "en.png"}             onClick={() => changeLanguage(i18n.language =="cs" ? "en" : "cs")} />
            <img className="w-[40px] cursor-pointer" src={mode ? "zmena_modu_bila.png" : "zmena_modu.png"} onClick={() => dispatch(toggleMode())} />
          </div>
        </div>
        <p className={clsx("mb-8 mt-4 w-full text-center text-4xl font-bold md:hidden", mode ? "text-white" : "")}>
          CHANGE
          <span className={clsx(!mode ? "text-light_blue" : "text-white", "block")}>THE TEXT.</span>
        </p>
      </>
    </div>
  )
}
