import DOMPurify from "dompurify"

export const sntz = (thing: any)=>{ //function that sanitizes inputs against XXS attacks
  return(DOMPurify.sanitize(thing))
}
