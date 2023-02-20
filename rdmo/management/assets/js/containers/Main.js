import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import isEmpty from 'lodash/isEmpty';
import * as configActions from '../actions/configActions'
import * as elementActions from '../actions/elementActions'
import isNil from 'lodash/isNil'

import ApiErrors from '../components/ApiErrors'

import Catalogs from '../components/elements/Catalogs'
import Catalog from '../components/elements/Catalog'
import Pages from '../components/elements/Pages'
import Page from '../components/elements/Page'
import Questions from '../components/elements/Questions'
import Question from '../components/elements/Question'
import QuestionSets from '../components/elements/QuestionSets'
import QuestionSet from '../components/elements/QuestionSet'
import Sections from '../components/elements/Sections'
import Section from '../components/elements/Section'

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
