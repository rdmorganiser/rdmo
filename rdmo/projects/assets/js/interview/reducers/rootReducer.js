import { combineReducers } from 'redux'

import configReducer from './configReducer'

const rootReducer = combineReducers({
  config: configReducer
})

export default rootReducer
