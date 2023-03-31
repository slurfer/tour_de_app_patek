import { combineReducers } from "redux"

import { darkModeReducer } from "./dark_mode_reducer"
import { notesReducer } from "./notes_reducer"

export default combineReducers({
  notes: notesReducer,
  mode: darkModeReducer
})
