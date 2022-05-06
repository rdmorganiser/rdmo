import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import * as questionsActions from '../actions/questionsActions'


const Sidebar = ({ questionsActions }) => {
  return <button className="btn btn-primary"
                 onClick={() => questionsActions.fetchCatalog(1)}>Fetch catalog</button>
}

Sidebar.propTypes = {
  questionsActions: PropTypes.object.isRequired
}

function mapStateToProps(state, props) {
  return {}
}

function mapDispatchToProps(dispatch) {
  return {
    questionsActions: bindActionCreators(questionsActions, dispatch)
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Sidebar)
