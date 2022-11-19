import { combineReducers } from 'redux'

import configReducer from './configReducer'
import elementsReducer from './elementsReducer'

const createRootReducer = () => combineReducers({
  config: configReducer,
  elements: elementsReducer
})

export default createRootReducer
