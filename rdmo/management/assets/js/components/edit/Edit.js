import React from 'react'
import { useSelector } from 'react-redux'

import useScrollEffect from '../../hooks/useScrollEffect'

import EditAttribute from './EditAttribute'
import EditCatalog from './EditCatalog'
import EditCondition from './EditCondition'
import EditOption from './EditOption'
import EditOptionSet from './EditOptionSet'
import EditPage from './EditPage'
import EditQuestion from './EditQuestion'
import EditQuestionSet from './EditQuestionSet'
import EditSection from './EditSection'
import EditTask from './EditTask'
import EditView from './EditView'

const Edit = () => {
  const { element, elementType } = useSelector((state) => state.elements)

  useScrollEffect(elementType, element.id)

  switch (elementType) {
    case 'catalogs':
      return <EditCatalog catalog={element} />
    case 'sections':
      return <EditSection section={element} />
    case 'pages':
      return <EditPage page={element} />
    case 'questionsets':
      return <EditQuestionSet questionset={element}  />
    case 'questions':
      return <EditQuestion question={element} />
    case 'attributes':
      return <EditAttribute attribute={element}  />
    case 'optionsets':
      return <EditOptionSet optionset={element} />
    case 'options':
      return <EditOption option={element} />
    case 'conditions':
      return <EditCondition condition={element} />
    case 'tasks':
      return <EditTask task={element} />
    case 'views':
      return <EditView view={element} />
  }
}

export default Edit
