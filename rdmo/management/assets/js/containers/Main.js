import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import isEmpty from 'lodash/isEmpty';
import * as configActions from '../actions/configActions'
import * as elementActions from '../actions/elementActions'
import isNil from 'lodash/isNil'

import ApiErrors from '../components/ApiErrors'

import Attributes from '../components/elements/Attributes'
import Catalogs from '../components/elements/Catalogs'
import Conditions from '../components/elements/Conditions'
import Options from '../components/elements/Options'
import OptionSets from '../components/elements/OptionSets'
import Pages from '../components/elements/Pages'
import Questions from '../components/elements/Questions'
import QuestionSets from '../components/elements/QuestionSets'
import Sections from '../components/elements/Sections'
import Tasks from '../components/elements/Tasks'
import Views from '../components/elements/Views'

import EditAttribute from '../components/edit/EditAttribute'
import EditCatalog from '../components/edit/EditCatalog'
import EditCondition from '../components/edit/EditCondition'
import EditOption from '../components/edit/EditOption'
import EditOptionSet from '../components/edit/EditOptionSet'
import EditPage from '../components/edit/EditPage'
import EditQuestion from '../components/edit/EditQuestion'
import EditQuestionSet from '../components/edit/EditQuestionSet'
import EditSection from '../components/edit/EditSection'
import EditTask from '../components/edit/EditTask'
import EditView from '../components/edit/EditView'

import NestedAttribute from '../components/nested/NestedAttribute'
import NestedCatalog from '../components/nested/NestedCatalog'
import NestedOptionSet from '../components/nested/NestedOptionSet'
import NestedPage from '../components/nested/NestedPage'
import NestedQuestionSet from '../components/nested/NestedQuestionSet'
import NestedSection from '../components/nested/NestedSection'

class Main extends Component {

  constructor(props) {
    super(props)
  }

  render() {
    const { config, elements, errors, elementActions } = this.props

    if (!isNil(elements.errors) && !isNil(elements.errors.api)) {
      return <ApiErrors errors={elements.errors.api} />
    } else {
      const element = elements.element

      switch (elements.elementType) {
        case 'catalogs':
          if (isNil(elements.element)) {
            return <Catalogs
              config={config} catalogs={elements.catalogs} fetchElement={elementActions.fetchElement}
              createElement={elementActions.createElement} storeElement={elementActions.storeElement} />
          } else if (elements.elementAction == 'nested') {
            return <NestedCatalog
              config={config} catalog={element}
              fetchElement={elementActions.fetchElement} storeElement={elementActions.storeElement} />
          } else {
            return <EditCatalog
              config={config} catalog={element}
              sites={elements.sites} groups={elements.groups} sections={elements.sections}
              updateElement={elementActions.updateElement} storeElement={elementActions.storeElement} />
          }
        case 'sections':
          if (isNil(elements.element)) {
            return <Sections
              config={config} sections={elements.sections} fetchElement={elementActions.fetchElement}
              createElement={elementActions.createElement} storeElement={elementActions.storeElement} />
          } else if (elements.elementAction == 'nested') {
            return <NestedSection
              config={config} section={element}
              fetchElement={elementActions.fetchElement} storeElement={elementActions.storeElement} />
          } else {
            return <EditSection
              config={config} section={element} pages={elements.pages}
              updateElement={elementActions.updateElement} storeElement={elementActions.storeElement} />
          }
        case 'pages':
          if (isNil(elements.element)) {
            return <Pages
              config={config} pages={elements.pages} fetchElement={elementActions.fetchElement}
              createElement={elementActions.createElement} storeElement={elementActions.storeElement} />
          } else if (elements.elementAction == 'nested') {
            return <NestedPage
              config={config} page={element}
              fetchElement={elementActions.fetchElement} storeElement={elementActions.storeElement} />
          } else {
            return <EditPage
              config={config} page={element}
              attributes={elements.attributes} conditions={elements.conditions}
              questionsets={elements.questionsets} questions={elements.questions}
              updateElement={elementActions.updateElement} storeElement={elementActions.storeElement} />
          }
        case 'questionsets':
          if (isNil(elements.element)) {
            return <QuestionSets
              config={config} questionsets={elements.questionsets} fetchElement={elementActions.fetchElement}
              createElement={elementActions.createElement} storeElement={elementActions.storeElement} />
          } else if (elements.elementAction == 'nested') {
            return <NestedQuestionSet
              config={config} questionset={element}
              fetchElement={elementActions.fetchElement} storeElement={elementActions.storeElement} />
          } else {
            return <EditQuestionSet
              config={config} questionset={element}
              attributes={elements.attributes} conditions={elements.conditions}
              questionsets={elements.questionsets} questions={elements.questions}
              updateElement={elementActions.updateElement} storeElement={elementActions.storeElement} />
          }
        case 'questions':
          if (isNil(elements.element)) {
            return <Questions
              config={config} questions={elements.questions} fetchElement={elementActions.fetchElement}
              createElement={elementActions.createElement} storeElement={elementActions.storeElement} />
          } else {
            return <EditQuestion
              config={config} question={element}
              attributes={elements.attributes} conditions={elements.conditions}
              optionsets={elements.optionsets} options={elements.options}
              widgetTypes={elements.widgetTypes} valueTypes={elements.valueTypes}
              updateElement={elementActions.updateElement} storeElement={elementActions.storeElement} />
          }
        case 'attributes':
          if (isNil(elements.element)) {
            return <Attributes
              config={config} attributes={elements.attributes} fetchElement={elementActions.fetchElement}
              createElement={elementActions.createElement} storeElement={elementActions.storeElement} />
          } else if (elements.elementAction == 'nested') {
            return <NestedAttribute
              config={config} attribute={element}
              fetchElement={elementActions.fetchElement} storeElement={elementActions.storeElement} />
          } else {
            return <EditAttribute
              config={config} attribute={element} attributes={elements.attributes}
              updateElement={elementActions.updateElement} storeElement={elementActions.storeElement} />
          }
        case 'optionsets':
          if (isNil(elements.element)) {
            return <OptionSets
              config={config} optionsets={elements.optionsets} fetchElement={elementActions.fetchElement}
              createElement={elementActions.createElement} storeElement={elementActions.storeElement} />
          } else if (elements.elementAction == 'nested') {
            return <NestedOptionSet
              config={config} optionset={element}
              fetchElement={elementActions.fetchElement} storeElement={elementActions.storeElement} />
          } else {
            return <EditOptionSet
              config={config} optionset={element}
              options={elements.options} providers={elements.providers}
              updateElement={elementActions.updateElement} storeElement={elementActions.storeElement} />
          }
        case 'options':
          if (isNil(elements.element)) {
            return <Options
              config={config} options={elements.options} fetchElement={elementActions.fetchElement}
              createElement={elementActions.createElement} storeElement={elementActions.storeElement} />
          } else {
            return <EditOption
              config={config} option={element}
              updateElement={elementActions.updateElement} storeElement={elementActions.storeElement} />
          }
        case 'conditions':
          if (isNil(elements.element)) {
            return <Conditions
              config={config} conditions={elements.conditions} fetchElement={elementActions.fetchElement}
              createElement={elementActions.createElement} storeElement={elementActions.storeElement} />
          } else {
            return <EditCondition
              config={config} condition={element} relations={elements.relations}
              attributes={elements.attributes} options={elements.options}
              updateElement={elementActions.updateElement} storeElement={elementActions.storeElement} />
          }
        case 'tasks':
          if (isNil(elements.element)) {
            return <Tasks
              config={config} tasks={elements.tasks} fetchElement={elementActions.fetchElement}
              createElement={elementActions.createElement} storeElement={elementActions.storeElement} />
          } else {
            return <EditTask
              config={config} task={element}
              attributes={elements.attributes} conditions={elements.conditions}
              catalogs={elements.catalogs} groups={elements.groups} sites={elements.sites}
              updateElement={elementActions.updateElement} storeElement={elementActions.storeElement} />
          }
        case 'views':
          if (isNil(elements.element)) {
            return <Views
              config={config} views={elements.views} fetchElement={elementActions.fetchElement}
              createElement={elementActions.createElement} storeElement={elementActions.storeElement} />
          } else {
            return <EditView
              config={config} view={element}
              catalogs={elements.catalogs} groups={elements.groups} sites={elements.sites}
              updateElement={elementActions.updateElement} storeElement={elementActions.storeElement} />
          }
        default:
          return null
      }
    }
  }

}

Main.propTypes = {
  config: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

function mapStateToProps(state, props) {
  return {
    config: state.config,
    elements: state.elements
  }
}

function mapDispatchToProps(dispatch) {
  return {
    configActions: bindActionCreators(configActions, dispatch),
    elementActions: bindActionCreators(elementActions, dispatch)
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Main)
