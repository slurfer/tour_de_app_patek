import { combineReducers } from "redux"

import { darkModeReducer } from "./dark_mode_reducer"
import { usersReducer } from "./users_reducer"

export default combineReducers({
  users: usersReducer,
  mode: darkModeReducer
})
