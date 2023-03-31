import axios from "axios"
import { baseUrl } from "../../constants"

export const getRequest = async (path:string, token?:string) => {
  
  const headers = {
    "x-access-token": token?token:""
  }

  try {
    const response = await axios.get(`${baseUrl}/${path}`,{headers})
    return(response.data)
  } catch (error) {
    console.error(error)
  }
}