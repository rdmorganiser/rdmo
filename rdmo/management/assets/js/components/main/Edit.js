import React from 'react'
import PropTypes from 'prop-types'

import EditAttribute from '../edit/EditAttribute'
import EditCatalog from '../edit/EditCatalog'
import EditCondition from '../edit/EditCondition'
import EditOption from '../edit/EditOption'
import EditOptionSet from '../edit/EditOptionSet'
import EditPage from '../edit/EditPage'
import EditQuestion from '../edit/EditQuestion'
import EditQuestionSet from '../edit/EditQuestionSet'
import EditSection from '../edit/EditSection'
import EditTask from '../edit/EditTask'
import EditView from '../edit/EditView'

import useScrollEffect from '../../hooks/useScrollEffect'

const Edit = ({ config, elements, elementActions }) => {
  const { element, elementType } = elements

  useScrollEffect(elementType, element.id)

  switch (elementType) {
    case 'catalogs':
      return <EditCatalog config={config} catalog={element} elements={elements} elementActions={elementActions} />
    case 'sections':
      return <EditSection config={config} section={element} elements={elements} elementActions={elementActions} />
    case 'pages':
      return <EditPage config={config} page={element} elements={elements} elementActions={elementActions} />
    case 'questionsets':
      return <EditQuestionSet config={config} questionset={element} elements={elements} elementActions={elementActions} />
    case 'questions':
      return <EditQuestion config={config} question={element} elements={elements} elementActions={elementActions} />
    case 'attributes':
      return <EditAttribute config={config} attribute={element} elements={elements} elementActions={elementActions} />
    case 'optionsets':
      return <EditOptionSet config={config} optionset={element} elements={elements} elementActions={elementActions} />
    case 'options':
      return <EditOption config={config} option={element} elements={elements} elementActions={elementActions} />
    case 'conditions':
      return <EditCondition config={config} condition={element} elements={elements} elementActions={elementActions} />
    case 'tasks':
      return <EditTask config={config} task={element} elements={elements} elementActions={elementActions} />
    case 'views':
      return <EditView config={config} view={element} elements={elements} elementActions={elementActions} />
  }
}

Edit.propTypes = {
  config: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Edit
