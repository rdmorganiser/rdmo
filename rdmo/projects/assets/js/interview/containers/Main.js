import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import Breadcrump from '../components/Breadcrump'
import Page from '../components/Page'

import * as configActions from '../actions/configActions'
import * as interviewActions from '../actions/interviewActions'

// eslint-disable-next-line no-unused-vars
const Main = ({ config, interview, configActions, interviewActions }) => {

  if (interview.show) {
    return (
      <div>
        <Breadcrump overview={interview.overview} page={interview.page} onClick={interviewActions.fetchPage} />
        <Page page={interview.page} />
      </div>
    )
  }

  // fetching the data is not complete yet, or no action was invoked yet
  return null
}

Main.propTypes = {
  config: PropTypes.object.isRequired,
  interview: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  interviewActions: PropTypes.object.isRequired
}

function mapStateToProps(state) {
  return {
    config: state.config,
    interview: state.interview
  }
}

function mapDispatchToProps(dispatch) {
  return {
    configActions: bindActionCreators(configActions, dispatch),
    interviewActions: bindActionCreators(interviewActions, dispatch),
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Main)
