import React from 'react'
import { DndProvider } from 'react-dnd'
import { HTML5Backend } from 'react-dnd-html5-backend'
import { createRoot } from 'react-dom/client'
import { Provider } from 'react-redux'

import Pending from '../../../core/assets/js/containers/Pending'

import configureStore from './interview/store/configureStore'

import Main from './interview/containers/Main'
import Sidebar from './interview/containers/Sidebar'

const store = configureStore()

createRoot(document.getElementById('main')).render(
  <DndProvider backend={HTML5Backend}>
    <Provider store={store}>
      <Main />
    </Provider>
  </DndProvider>
)

createRoot(document.getElementById('sidebar')).render(
  <Provider store={store}>
    <Sidebar />
  </Provider>
)

createRoot(document.getElementById('pending')).render(
  <Provider store={store}>
    <Pending />
  </Provider>
)
