import { combineReducers } from 'redux'
import projectsReducer from './projectsReducer'

const rootReducer = combineReducers({
  projects: projectsReducer,
})

export default rootReducer
