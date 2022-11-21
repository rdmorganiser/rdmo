import { combineReducers } from 'redux'

import configReducer from './configReducer'
import elementsReducer from './elementsReducer'

const rootReducer = combineReducers({
  config: configReducer,
  elements: elementsReducer
})

export default rootReducer
