import React from 'react'
import { useSelector } from 'react-redux'
import { get, isEmpty, isNil } from 'lodash'

import { MainErrors } from '../components/common/Errors'

import Edit from '../components/main/Edit'
import Elements from '../components/main/Elements'
import Import from '../components/main/Import'
import Nested from '../components/main/Nested'

const Main = () => {
  const config = useSelector((state) => state.config)
  const elements = useSelector((state) => state.elements)
  const imports = useSelector((state) => state.imports)

  const { element, elementType, elementId, elementAction } = elements

  // check if anything was loaded yet
  if (isNil(config.settings) || isNil(elementType)) {
    return null
  }

  // check if an error occurred
  if (!isNil(elements.errors.api)) {
    return <MainErrors errors={elements.errors.api} />
  } else if (get(elements, 'element.errors.api')) {
    return <MainErrors errors={get(elements, 'element.errors.api')} />
  } else if (!isNil(imports.errors.file)) {
    return <MainErrors errors={imports.errors.file} />
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

export default Main
