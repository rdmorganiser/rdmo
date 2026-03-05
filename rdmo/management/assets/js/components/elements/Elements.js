import React from 'react'
import { useSelector } from 'react-redux'

import Attributes from './Attributes'
import Catalogs from './Catalogs'
import Conditions from './Conditions'
import Options from './Options'
import OptionSets from './OptionSets'
import Pages from './Pages'
import Questions from './Questions'
import QuestionSets from './QuestionSets'
import Sections from './Sections'
import Tasks from './Tasks'
import Views from './Views'

import useScrollEffect from '../../hooks/useScrollEffect'

const Elements = () => {
  const { elementType } = useSelector((state) => state.elements)

  useScrollEffect(elementType)

  switch (elementType) {
    case 'catalogs':
      return <Catalogs  />
    case 'sections':
      return <Sections  />
    case 'pages':
      return <Pages  />
    case 'questionsets':
      return <QuestionSets  />
    case 'questions':
      return <Questions  />
    case 'attributes':
      return <Attributes  />
    case 'optionsets':
      return <OptionSets  />
    case 'options':
      return <Options  />
    case 'conditions':
      return <Conditions  />
    case 'tasks':
      return <Tasks  />
    case 'views':
      return <Views  />
  }
}

export default Elements
