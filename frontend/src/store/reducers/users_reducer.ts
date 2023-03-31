import { IUser } from "../../types"

export const usersReducer = (state: IUser[] = [], action: any) => {
  switch (action.type) {
  case "SET_USERS": {
    return action.users ? action.users : []
  }
  case "ADD_USER": {
    return [action.newuser, ...state]
  }
  case "REMOVE_USER": {
    return state.filter((user: IUser) => user.id !== action.deleteduser_id)
  }
  case "UPDATE_USER": {
    return state.map((record: IUser) => (record.id !== action.updated_user_id ? record : action.newrecord))
  }
  default:
    return state
  }
}
