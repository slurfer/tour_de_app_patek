export const darkModeReducer = (state = false, action: any) => {
  switch (action.type) {
  case "TOGGLE_DARK_MODE": {
    return !state
  }
  default:
    return state
  }
}
