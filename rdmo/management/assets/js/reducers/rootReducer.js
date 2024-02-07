import { combineReducers } from 'redux'

import configReducer from './configReducer'
import elementsReducer from './elementsReducer'
import importsReducer from './importsReducer'

const rootReducer = combineReducers({
  config: configReducer,
  elements: elementsReducer,
  imports: importsReducer
})

export default rootReducer
