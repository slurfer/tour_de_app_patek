import clsx from "clsx"

import { Button } from "../../src/types"

interface IFormButton {
  className: string
  text: string
  onClick?: any
  type?: Button
  main_color?: boolean
}

export const FormButton = ({ className, text, onClick, type }: IFormButton) => {
  return (
    <button
      className={clsx("m-auto w-[50%] rounded-2xl px-5 py-2 font-bold text-white hover:opacity-80", className)}
      onClick={onClick}
      type={type ? type : undefined}
    >
      {text}
    </button>
  )
}
