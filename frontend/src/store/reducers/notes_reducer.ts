import { ISticknote } from "../../types"

export const notesReducer = (state: ISticknote[] = [], action: any) => {
  switch (action.type) {
  case "SET_NOTES": {
    return action.notes ? action.notes : []
  }
  case "ADD_NOTE": {
    return [action.newnote, ...state]
  }
  case "REMOVE_NOTE": {
    return state.filter((user: ISticknote) => user.id !== action.deleteduser_id)
  }
  case "UPDATE_NOTE": {
    return state.map((record: ISticknote) => (record.id !== action.updated_user_id ? record : action.newrecord))
  }
  default:
    return state
  }
}
