import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import isEmpty from 'lodash/isEmpty';
import * as configActions from '../actions/configActions'
import * as elementActions from '../actions/elementActions'

import Errors from '../components/Errors'

import Catalogs from '../components/elements/Catalogs'
import Pages from '../components/elements/Pages'
import Questions from '../components/elements/Questions'
import QuestionSets from '../components/elements/QuestionSets'
import Sections from '../components/elements/Sections'

class Main extends Component {

  constructor(props) {
    super(props)
  }

  render() {
    const { config, elements } = this.props

    if (isEmpty(elements.errors)) {
      switch (elements.elementType) {
        case 'catalogs':
          return <Catalogs config={config} catalogs={elements.catalogs} />
        case 'sections':
          return <Sections config={config} sections={elements.sections} />
        case 'pages':
          return <Pages config={config} pages={elements.pages} />
        case 'questionsets':
          return <QuestionSets config={config} questionsets={elements.questionsets} />
        case 'questions':
          return <Questions config={config} questions={elements.questions} />
        default:
          return null
      }
    } else {
      return <Errors config={config} errors={elements.errors} />
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
