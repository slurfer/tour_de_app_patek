import { ISticknote } from "../src/types"
import { NewNote } from "./NewNote"
import { Sticknote } from "./Sticknote"

export const Sticknotes = ({data}:{data:ISticknote[]})=>{

  return(
    <div className="flex flex-wrap">
      <NewNote />
      {data.map((item)=>{
        return(
          <Sticknote 
            id={item.id}
            color={item.color}
            key={item.id}
            content={item.content}
            author={item.author}
          />)
      })}
    </div>
  )
}