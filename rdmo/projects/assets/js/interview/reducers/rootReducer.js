import { combineReducers } from 'redux'

import configReducer from './configReducer'
import pageReducer from './pageReducer'

const rootReducer = combineReducers({
  config: configReducer,
  page: pageReducer
})

export default rootReducer
