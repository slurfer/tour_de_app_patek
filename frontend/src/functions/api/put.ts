import axios from "axios"
import { baseUrl } from "../../constants"

export const putRequest = async (path:string,id: number, data: any)=> {

  try {
    const response = await axios.put(`${baseUrl}/${path}/${id}`, data)
    return(response.data)
  } catch (error) {
    console.error(error)
  }
}