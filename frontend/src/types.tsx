export type Language = "Python" | "Javascript" | "C++"
export type Rating = 1 | 2 | 3 | 4 | 5
export type MinutesSpent = number & { __isPositive: true }
export type Button = "button" | "submit" | "reset"
export type Sorting = "from newest" | "from oldest" | "from best rating" | "from worst rating" | "from shortest" | "from longest" | "no sorting"
export type Color = "red" | "orange" | "blue" | "yellow" | "green" | "purple" | "pink" | "brown"

export type ISticknote = {
  content: string,
  author:string,
  id:number,
  color:Color
}

export interface IDiaryEntry {
  date: string
  programming_language: string
  time_spent: MinutesSpent
  rating: Rating
  description: string
  programmer_id: number | null
  id: number
  tag_ids: number[]
}

export interface IUser {
  name: string
  surname: string
  username: string
  email: string
  id: number
  admin: boolean
  password: string | null
}

export interface ITag {
  name: string
  color: Color
  description: string
  id: number
}

export interface State {
  token?: string
  mode: boolean
  user: IUser
  tags: ITag[]
  users: IUser[]
  records: IDiaryEntry[]
}
