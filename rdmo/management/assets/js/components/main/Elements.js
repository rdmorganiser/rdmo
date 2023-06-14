import React from 'react'
import PropTypes from 'prop-types'

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

const Elements = ({ config, elements, configActions, elementActions }) => {
  const { elementType } = elements

  useScrollEffect(elementType)

  switch (elementType) {
    case 'catalogs':
      return <Catalogs config={config} catalogs={elements.catalogs}
                       configActions={configActions} elementActions={elementActions} />
    case 'sections':
      return <Sections config={config} sections={elements.sections}
                       configActions={configActions} elementActions={elementActions} />
    case 'pages':
      return <Pages config={config} pages={elements.pages}
                    configActions={configActions} elementActions={elementActions} />
    case 'questionsets':
      return <QuestionSets config={config} questionsets={elements.questionsets}
                           configActions={configActions} elementActions={elementActions} />
    case 'questions':
      return <Questions config={config} questions={elements.questions}
                        configActions={configActions} elementActions={elementActions} />
    case 'attributes':
      return <Attributes config={config} attributes={elements.attributes}
                         configActions={configActions} elementActions={elementActions} />
    case 'optionsets':
      return <OptionSets config={config} optionsets={elements.optionsets}
                         configActions={configActions} elementActions={elementActions} />
    case 'options':
      return <Options config={config} options={elements.options}
                      configActions={configActions} elementActions={elementActions} />
    case 'conditions':
      return <Conditions config={config} conditions={elements.conditions}
                         configActions={configActions} elementActions={elementActions} />
    case 'tasks':
      return <Tasks config={config} tasks={elements.tasks}
                    configActions={configActions} elementActions={elementActions} />
    case 'views':
      return <Views config={config} views={elements.views}
                    configActions={configActions} elementActions={elementActions} />
  }
}

Elements.propTypes = {
  config: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Elements
