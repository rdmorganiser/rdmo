import { applyMiddleware, compose, createStore } from 'redux'
import thunk from 'redux-thunk'

import createRootReducer from '../reducers/rootReducer'

export default function configureStore() {
  const store = createStore(
    createRootReducer(),
    compose(
      applyMiddleware(
        thunk
      ),
    ),
  )

  return store
}
