import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import * as configActions from '../actions/configActions'
import * as elementActions from '../actions/elementActions'

import Catalogs from '../components/Catalogs'
import Pages from '../components/Pages'
import Questions from '../components/Questions'
import QuestionSets from '../components/QuestionSets'
import Sections from '../components/Sections'

class Main extends Component {

  constructor(props) {
    super(props)
  }

  render() {
    const { config, elements } = this.props

    switch (config.resourceType) {
      case 'catalogs':
        return <Catalogs catalogs={elements.catalogs} />
      case 'sections':
        return <Sections sections={elements.sections} />
      case 'pages':
        return <Pages pages={elements.pages} />
      case 'questionsets':
        return <QuestionSets questionsets={elements.questionsets} />
      case 'questions':
        return <Questions questions={elements.questions} />
      default:
        return null
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
