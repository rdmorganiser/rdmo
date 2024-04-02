import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import Buttons from '../components/Buttons'
import Navigation from '../components/Navigation'
import Overview from '../components/Overview'
import Progress from '../components/Progress'

import * as configActions from '../actions/configActions'
import * as interviewActions from '../actions/interviewActions'

// eslint-disable-next-line no-unused-vars
const Sidebar = ({ config, interview, configActions, interviewActions }) => {
  if (interview.show) {
    return (
      <div>
        <Overview
          overview={interview.overview}
          help={config.templates.project_interview_overview_help}/>
        <Progress
          progress={interview.progress}
          help={config.templates.project_interview_progress_help} />
        <Buttons
          page={interview.page}
          help={config.templates.project_interview_buttons_help}
          onClick={interviewActions.fetchPage} />
        <Navigation
          page={interview.page}
          navigation={interview.navigation}
          help={config.templates.project_interview_navigation_help}
          onClick={interviewActions.fetchPage} />
      </div>
    )
  }

  // fetching the data is not complete yet, or no action was invoked yet
  return null
}

Sidebar.propTypes = {
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

export default connect(mapStateToProps, mapDispatchToProps)(Sidebar)
