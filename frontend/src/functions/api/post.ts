import axios from "axios"
import { baseUrl } from "../../constants"

export const postRequest = async (path: string ,data:any) => {

  const response = await axios.post(`${baseUrl}/${path}`, data )
  return(response.data)
}