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

import Attribute from '../components/element/Attribute'
import Catalog from '../components/element/Catalog'
import Condition from '../components/element/Condition'
import Option from '../components/element/Option'
import OptionSet from '../components/element/OptionSet'
import Page from '../components/element/Page'
import Question from '../components/element/Question'
import QuestionSet from '../components/element/QuestionSet'
import Section from '../components/element/Section'
import Task from '../components/element/Task'
import View from '../components/element/View'

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
          return isNil(element)
            ? <Catalogs
                config={config} catalogs={elements.catalogs}
                fetchCatalog={id => elementActions.fetchElement('catalogs', id)} />
            : <Catalog
                config={config} catalog={element}
                sites={elements.sites} groups={elements.groups}
                warnings={elements.warnings} errors={elements.errors}
                updateCatalog={(key, value) => elementActions.updateElement(element, key, value)}
                storeCatalog={() => elementActions.storeElement('catalogs', element)} />
        case 'sections':
          return isNil(element)
            ? <Sections
                config={config} sections={elements.sections}
                fetchSection={id => elementActions.fetchElement('sections', id)} />
            : <Section
                config={config} section={element}
                warnings={elements.warnings} errors={elements.errors}
                updateSection={(key, value) => elementActions.updateElement(element, key, value)}
                storeSection={() => elementActions.storeElement('sections', element)} />
        case 'pages':
          return isNil(element)
            ? <Pages
                config={config} pages={elements.pages}
                fetchPage={id => elementActions.fetchElement('pages', id)} />
            : <Page config={config} page={element}
                attributes={elements.attributes} conditions={elements.attributes}
                warnings={elements.warnings} errors={elements.errors}
                updatePage={(key, value) => elementActions.updateElement(element, key, value)}
                storePage={() => elementActions.storeElement('pages', element)} />
        case 'questionsets':
          return isNil(element)
            ? <QuestionSets
                config={config} questionsets={elements.questionsets}
                fetchQuestionSet={id => elementActions.fetchElement('questionsets', id)} />
            : <QuestionSet
                config={config} questionset={element}
                conditions={elements.attributes}
                warnings={elements.warnings} errors={elements.errors}
                updateQuestionSet={(key, value) => elementActions.updateElement(element, key, value)}
                storeQuestionSet={() => elementActions.storeElement('questionsets', element)} />
        case 'questions':
          return isNil(element)
            ? <Questions
                config={config} questions={elements.questions}
                fetchQuestion={id => elementActions.fetchElement('questions', id)} />
            : <Question
                config={config} question={element}
                attributes={elements.attributes} options={elements.options}
                widgetTypes={elements.widgetTypes} valueTypes={elements.valueTypes}
                warnings={elements.warnings} errors={elements.errors}
                updateQuestion={(key, value) => elementActions.updateElement(element, key, value)}
                storeQuestion={() => elementActions.storeElement('questions', element)} />
        case 'attributes':
          return isNil(element)
            ? <Attributes
                config={config} attributes={elements.attributes}
                fetchAttribute={id => elementActions.fetchElement('attributes', id)} />
            : <Attribute
                config={config} attribute={element}
                attributes={elements.attributes}
                warnings={elements.warnings} errors={elements.errors}
                updateAttribute={(key, value) => elementActions.updateElement(element, key, value)}
                storeAttribute={() => elementActions.storeElement('attributes', element)} />
        case 'optionsets':
          return isNil(element)
            ? <OptionSets
                config={config} optionsets={elements.optionsets}
                fetchOptionSet={id => elementActions.fetchElement('optionsets', id)} />
            : <OptionSet
                config={config} optionset={element}
                providers={elements.providers}
                warnings={elements.warnings} errors={elements.errors}
                updateOptionSet={(key, value) => elementActions.updateElement(element, key, value)}
                storeOptionSet={() => elementActions.storeElement('optionsets', element)} />
        case 'options':
          return isNil(element)
            ? <Options
                config={config} options={elements.options}
                fetchOption={id => elementActions.fetchElement('options', id)} />
            : <Option
                config={config} option={element}
                warnings={elements.warnings} errors={elements.errors}
                updateOption={(key, value) => elementActions.updateElement(element, key, value)}
                storeOption={() => elementActions.storeElement('options', element)} />
        case 'conditions':
          return isNil(element)
            ? <Conditions
                config={config} conditions={elements.conditions}
                fetchCondition={id => elementActions.fetchElement('conditions', id)} />
            : <Condition
                config={config} condition={element}
                warnings={elements.warnings} errors={elements.errors}
                relations={elements.relations} attributes={elements.attributes} options={elements.options}
                updateCondition={(key, value) => elementActions.updateElement(element, key, value)}
                storeCondition={() => elementActions.storeElement('conditions', element)} />
        case 'tasks':
          return isNil(element)
            ? <Tasks
                config={config} tasks={elements.tasks}
                fetchTask={id => elementActions.fetchElement('tasks', id)} />
            : <Task
                config={config} task={element}
                warnings={elements.warnings} errors={elements.errors}
                attributes={elements.attributes} catalogs={elements.catalogs}
                groups={elements.groups} sites={elements.sites}
                updateTask={(key, value) => elementActions.updateElement(element, key, value)}
                storeTask={() => elementActions.storeElement('tasks', element)} />
        case 'views':
          return isNil(element)
            ? <Views
                config={config} views={elements.views}
                fetchView={id => elementActions.fetchElement('views', id)} />
            : <View
                config={config} view={element}
                warnings={elements.warnings} errors={elements.errors}
                catalogs={elements.catalogs} groups={elements.groups} sites={elements.sites}
                updateView={(key, value) => elementActions.updateElement(element, key, value)}
                storeView={() => elementActions.storeElement('views', element)} />
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
