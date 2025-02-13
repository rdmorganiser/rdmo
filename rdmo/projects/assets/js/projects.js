import React from 'react'
import { createRoot } from 'react-dom/client'
import { Provider } from 'react-redux'

import configureStore from './projects/store/configureStore'

import { DndProvider } from 'react-dnd'
import { HTML5Backend } from 'react-dnd-html5-backend'

import Pending from '../../../core/assets/js/containers/Pending'

import Main from './projects/containers/Main'

const store = configureStore()

createRoot(document.getElementById('main')).render(
  <DndProvider backend={HTML5Backend}>
    <Provider store={store}>
      <Main />
    </Provider>
  </DndProvider>
)

createRoot(document.getElementById('pending')).render(
  <Provider store={store}>
    <Pending />
  </Provider>
)
