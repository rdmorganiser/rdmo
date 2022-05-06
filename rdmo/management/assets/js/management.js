import React from "react"
import ReactDOM from "react-dom"
import { createStore, applyMiddleware } from 'redux'
import { Provider } from 'react-redux'
import thunk from 'redux-thunk'
import ls from 'local-storage'

import rootReducer from './reducers/rootReducer'

import Main from './containers/Main'
import Sidebar from './containers/Sidebar'

const store = createStore(rootReducer, applyMiddleware(thunk))

ReactDOM.render(<Provider store={store}><Main /></Provider>, document.getElementById('main'))
ReactDOM.render(<Provider store={store}><Sidebar /></Provider>, document.getElementById('sidebar'))
