import clsx from "clsx"

import { inputSameProperties } from "../../src/constants"
import { Description } from "../Description"

interface IUniversalInput {
  text: string
  min?: number
  max?: boolean
  value: any
  onChange: any
  extrastyle?: string
  type?: any
  required?: boolean
  autofocus?: boolean
}

export const UniversalInput = ({ text, min, value, onChange, extrastyle, type, max, required, autofocus }: IUniversalInput) => {
  return (
    <>
      <Description text={text + (required ? " *" : "")} />
      <input
        className={clsx(inputSameProperties, extrastyle)}
        type={type ? type : "string"}
        min={min ? min : ""}
        maxLength={max ? 12 : undefined}
        value={value}
        onChange={onChange}
        required={required ? true : false}
        autoFocus={autofocus && true}
      />
    </>
  )
}
