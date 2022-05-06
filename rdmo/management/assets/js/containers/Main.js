import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import * as questionsActions from '../actions/questionsActions'

import Catalog from '../components/Catalog'

const Main = ({ questions, questionsActions }) => {
  if (questions.catalog !== null) {
    return <Catalog catalog={questions.catalog} />
  } else {
    return null
  }
}

Main.propTypes = {
  questions: PropTypes.object.isRequired,
  questionsActions: PropTypes.object.isRequired
}

function mapStateToProps(state, props) {
  return {
    questions: state.questions
  }
}

function mapDispatchToProps(dispatch) {
  return {
    questionsActions: bindActionCreators(questionsActions, dispatch)
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Main)
