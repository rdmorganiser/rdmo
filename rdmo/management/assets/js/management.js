import React from "react"
import ReactDOM from "react-dom"
import { Provider } from 'react-redux'

import configureStore from './store/configureStore'
import addEventListener from './store/addEventListener'

import Main from './containers/Main'
import Sidebar from './containers/Sidebar'

const store = configureStore()

addEventListener(store.dispatch, store.getState)

ReactDOM.render(<Provider store={store}><Main /></Provider>, document.getElementById('main'))
ReactDOM.render(<Provider store={store}><Sidebar /></Provider>, document.getElementById('sidebar'))
