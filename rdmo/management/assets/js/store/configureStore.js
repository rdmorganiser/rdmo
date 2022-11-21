import { applyMiddleware, compose, createStore } from 'redux'
import thunk from 'redux-thunk'

import rootReducer from '../reducers/rootReducer'

export default function configureStore() {
  const store = createStore(
    rootReducer,
    applyMiddleware(thunk)
  )

  return store
}
