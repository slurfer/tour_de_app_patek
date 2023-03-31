import { AnyAction } from "redux"

import { ISticknote } from "../../types"

export const setNotes = (notes: Array<ISticknote>): AnyAction => {
  return {
    type: "SET_NOTES",
    notes: notes
  }
}

export const addSingleNote = (newnote: ISticknote): AnyAction => {
  return {
    type: "ADD_NOTE",
    newnote: newnote
  }
}

export const removeSingleNote = (deleteduser_id: number): AnyAction => {
  return {
    type: "REMOVE_NOTE",
    deleteduser_id: deleteduser_id
  }
}

export const updateSingleNote = (updated_user_id: number, newrecord: ISticknote): AnyAction => {
  return {
    type: "UPDATE_NOTE",
    updated_user_id: updated_user_id,
    newrecord: newrecord
  }
}

export const toggleMode = (): AnyAction => {
  return {
    type: "TOGGLE_DARK_MODE"
  }
}
