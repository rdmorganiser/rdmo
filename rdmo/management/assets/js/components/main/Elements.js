import React from 'react'
import { useSelector } from 'react-redux'

import Attributes from '../elements/Attributes'
import Catalogs from '../elements/Catalogs'
import Conditions from '../elements/Conditions'
import Options from '../elements/Options'
import OptionSets from '../elements/OptionSets'
import Pages from '../elements/Pages'
import Questions from '../elements/Questions'
import QuestionSets from '../elements/QuestionSets'
import Sections from '../elements/Sections'
import Tasks from '../elements/Tasks'
import Views from '../elements/Views'

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
