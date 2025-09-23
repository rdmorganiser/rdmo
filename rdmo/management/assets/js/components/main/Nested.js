import React from 'react'
import { useSelector } from 'react-redux'

import NestedAttribute from '../nested/NestedAttribute'
import NestedCatalog from '../nested/NestedCatalog'
import NestedOptionSet from '../nested/NestedOptionSet'
import NestedPage from '../nested/NestedPage'
import NestedQuestionSet from '../nested/NestedQuestionSet'
import NestedSection from '../nested/NestedSection'

import useScrollEffect from '../../hooks/useScrollEffect'

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
