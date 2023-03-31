import { AnyAction } from "redux"

import { IUser } from "../../types"

export const setUsers = (users: Array<IUser>): AnyAction => {
  return {
    type: "SET_USERS",
    users: users
  }
}

export const addSingleUser = (newuser: IUser): AnyAction => {
  return {
    type: "ADD_USER",
    newuser: newuser
  }
}

export const removeSingleUser = (deleteduser_id: number): AnyAction => {
  return {
    type: "REMOVE_USER",
    deleteduser_id: deleteduser_id
  }
}

export const updateSingleUser = (updated_user_id: number, newrecord: IUser): AnyAction => {
  return {
    type: "UPDATE_USER",
    updated_user_id: updated_user_id,
    newrecord: newrecord
  }
}

export const toggleMode = (): AnyAction => {
  return {
    type: "TOGGLE_DARK_MODE"
  }
}
