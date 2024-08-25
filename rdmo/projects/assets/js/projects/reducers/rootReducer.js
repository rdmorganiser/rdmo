import { combineReducers } from 'redux'
import configReducer from './configReducer'
import projectsReducer from './projectsReducer'
import userReducer from './userReducer'

const rootReducer = combineReducers({
  config: configReducer,
  currentUser: userReducer,
  projects: projectsReducer,
})

export default rootReducer
