/* eslint-disable @next/next/no-img-element */
/* eslint-disable jsx-a11y/alt-text */

import clsx from "clsx"
import { useSelector } from "react-redux"
import { motion } from "framer-motion"
import { State } from "../../src/types"

interface IUniversalForm {
  header: any
  onSubmit?: any
  closeForm: any
  children: any
  className?: string
}

export const UniversalForm = ({ header, onSubmit, children, closeForm, className }: IUniversalForm) => {
  const { mode } = useSelector((state: State) => state)

  return (
    <div
      className={clsx(
        "fixed left-0 top-0 h-screen w-screen overflow-hidden overflow-y-scroll px-10 py-[10px] lg:px-0",
        className,
        mode ? "bg-black/50" : "bg-black/80"
      )}
    >
      <form className={"relative m-auto w-[300px] rounded-xl border border-black bg-white p-10 text-black sm:w-[500px]"} onSubmit={onSubmit}>
        <motion.img           
          whileHover={{ scale:1.3 }}
          className="relative bottom-[15px] left-[220px] cursor-pointer sm:left-[415px]" src="zavrit_formular.png" onClick={closeForm}
        />
        <p className="mb-5 text-center text-2xl">{header}</p>
        <div className="overflow-hidden">{children}</div>
      </form>
    </div>
  )
}
