import React from 'react'
import PropTypes from 'prop-types'

import NestedAttribute from '../nested/NestedAttribute'
import NestedCatalog from '../nested/NestedCatalog'
import NestedOptionSet from '../nested/NestedOptionSet'
import NestedPage from '../nested/NestedPage'
import NestedQuestionSet from '../nested/NestedQuestionSet'
import NestedSection from '../nested/NestedSection'

import useScrollEffect from '../../hooks/useScrollEffect'

const Nested = ({ config, elements, configActions, elementActions }) => {
  const { element, elementType } = elements

  useScrollEffect(elementType, element.id, 'nested')

  switch (elementType) {
    case 'catalogs':
      return <NestedCatalog config={config} catalog={element}
                            configActions={configActions} elementActions={elementActions} />
    case 'sections':
      return <NestedSection config={config} section={element}
                            configActions={configActions} elementActions={elementActions} />
    case 'pages':
      return <NestedPage config={config} page={element}
                         configActions={configActions} elementActions={elementActions} />
    case 'questionsets':
      return <NestedQuestionSet config={config} questionset={element}
                                configActions={configActions} elementActions={elementActions} />
    case 'attributes':
      return <NestedAttribute config={config} attribute={element}
                              configActions={configActions} elementActions={elementActions} />
    case 'optionsets':
      return <NestedOptionSet config={config} optionset={element}
                              configActions={configActions} elementActions={elementActions} />
  }
}

Nested.propTypes = {
  config: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Nested
