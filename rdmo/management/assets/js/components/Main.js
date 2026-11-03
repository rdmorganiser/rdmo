import React from 'react'
import { useSelector } from 'react-redux'
import { isEmpty, isNil } from 'lodash'

import Errors from 'rdmo/core/assets/js/components/Errors'

import Edit from '../components/edit/Edit'
import Elements from '../components/elements/Elements'
import Import from '../components/import/Import'
import Nested from '../components/nested/Nested'

const Main = () => {
  const settings = useSelector((state) => state.settings)
  const constants = useSelector((state) => state.constants)
  const elements = useSelector((state) => state.elements)
  const imports = useSelector((state) => state.imports)
  const errors = useSelector((state) => state.errors)

  const { element, elementType, elementId, elementAction } = elements

  const render = () => {
    // check if anything was loaded yet
    if (isEmpty(settings) || isNil(constants.meta) || isNil(elementType)) {
      return null
    }

    // check if an error occurred
    if (errors.elements || errors.imports) {
      return null
    }

    if (!isEmpty(imports.elements)) {
      return <Import />
    }

    // check if the nested components should be displayed
    if (!isNil(element) && elementAction === 'nested') {
      return <Nested />
    }

    // check if the edit components should be displayed
    if (!isNil(element)) {
      return <Edit />
    }

    // check if the list components should be displayed
    if (isNil(elementId) && isNil(elementAction)) {
      return <Elements />
    }

    // fetching the data is not complete yet, or no action was invoked yet
    return null
  }

  return (
    <div className="container-lg gx-0">
      <Errors />
      {render()}
    </div>
  )
}

export default Main
