import React from 'react'
import { useSelector } from 'react-redux'

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
