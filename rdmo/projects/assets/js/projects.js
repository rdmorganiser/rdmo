import React from 'react'
import { createRoot } from 'react-dom/client'
import { Provider } from 'react-redux'

import configureStore from './store/configureStore'

import { DndProvider } from 'react-dnd'
import { HTML5Backend } from 'react-dnd-html5-backend'

import Main from './containers/Main'

const store = configureStore()

console.log('projects.js')
createRoot(document.getElementById('main')).render(
  <DndProvider backend={HTML5Backend}>
    <Provider store={store}>
      <Main />
    </Provider>
  </DndProvider>
)
