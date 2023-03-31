import { inputSameProperties, colorsNames } from "../../src/constants"
import clsx from "clsx"

interface ISelectColor {
    text:string
    value:any,
    onChange:any,
    bonusOption?:boolean
    color?:string
}

export const SelectColor = ({value,onChange,color}:ISelectColor)=>{

  return(
    <>
      <select 
        className={clsx(inputSameProperties,"m-auto w-fit border-2")} 
        value={value} 
        onChange={onChange}>
        {color&&<option key={0} value={color}>{color}</option>}
        {colorsNames.map(color =>{
          return(
            <option className="text-center" key={color} value={color}>{color}</option>
          )
        })}
      </select>
    </>
  )
}