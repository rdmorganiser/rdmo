import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import { isReady } from '../utils/interview'

import Buttons from '../components/sidebar/Buttons'
import Navigation from '../components/sidebar/Navigation'
import Overview from '../components/sidebar/Overview'
import Progress from '../components/sidebar/Progress'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'

import * as interviewActions from '../actions/interviewActions'

// eslint-disable-next-line no-unused-vars
const Sidebar = ({ config, settings, templates, user, project, interview, configActions, interviewActions }) => {
  if (isReady(interview)) {
    return (
      <div>
        <Overview
          overview={project.overview}
          help={templates.project_interview_overview_help}/>
        <Progress
          progress={project.progress}
          help={templates.project_interview_progress_help} />
        <Buttons
          prev={interview.page.prev_page}
          next={interview.page.next_page}
          help={templates.project_interview_buttons_help}
          fetchPage={interviewActions.fetchPage} />
        <Navigation
          currentPage={interview.page}
          navigation={interview.navigation}
          help={templates.project_interview_navigation_help}
          fetchPage={interviewActions.fetchPage} />
      </div>
    )
  }

  // fetching the data is not complete yet, or no action was invoked yet
  return null
}

Sidebar.propTypes = {
  config: PropTypes.object.isRequired,
  settings: PropTypes.object.isRequired,
  templates: PropTypes.object.isRequired,
  user: PropTypes.object.isRequired,
  project: PropTypes.object.isRequired,
  interview: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  interviewActions: PropTypes.object.isRequired
}

function mapStateToProps(state) {
  return {
    config: state.config,
    settings: state.settings,
    templates: state.templates,
    user: state.user,
    project: state.project,
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
