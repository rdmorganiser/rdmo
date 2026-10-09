import React from 'react'
import { useSelector } from 'react-redux'

import useScrollEffect from '../../hooks/useScrollEffect'

import NestedAttribute from './NestedAttribute'
import NestedCatalog from './NestedCatalog'
import NestedOptionSet from './NestedOptionSet'
import NestedPage from './NestedPage'
import NestedQuestionSet from './NestedQuestionSet'
import NestedSection from './NestedSection'

const Nested = () => {
  const { element, elementType } = useSelector((state) => state.elements)

  useScrollEffect(elementType, element.id, 'nested')

  switch (elementType) {
    case 'catalogs':
      return <NestedCatalog catalog={element} />
    case 'sections':
      return <NestedSection section={element} />
    case 'pages':
      return <NestedPage page={element} />
    case 'questionsets':
      return <NestedQuestionSet questionset={element} />
    case 'attributes':
      return <NestedAttribute attribute={element} />
    case 'optionsets':
      return <NestedOptionSet optionset={element} />
  }
}

export default Nested
