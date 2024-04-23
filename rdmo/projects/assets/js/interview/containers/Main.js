import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import Breadcrump from '../components/main/Breadcrump'
import Page from '../components/main/page/Page'

import { showInterview } from '../utils/interview'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'

import * as interviewActions from '../actions/interviewActions'

// eslint-disable-next-line no-unused-vars
const Main = ({ config, settings, templates, user, interview, configActions, interviewActions }) => {
  if (showInterview(interview)) {
    return (
      <div>
        <Breadcrump
          overview={interview.overview}
          currentPage={interview.page}
          fetchPage={interviewActions.fetchPage}
        />
        <Page
          config={config}
          templates={templates}
          page={interview.page}
          sets={interview.sets}
          values={interview.values}
          fetchPage={interviewActions.fetchPage}
          createValue={interviewActions.createValue}
          updateValue={interviewActions.updateValue}
          deleteValue={interviewActions.deleteValue}
          activateSet={interviewActions.activateSet}
          createSet={interviewActions.createSet}
          updateSet={interviewActions.updateSet}
          deleteSet={interviewActions.deleteSet}
        />
      </div>
    )
  }

  // fetching the data is not complete yet, or no action was invoked yet
  return null
}

Main.propTypes = {
  config: PropTypes.object.isRequired,
  settings: PropTypes.object.isRequired,
  templates: PropTypes.object.isRequired,
  user: PropTypes.object.isRequired,
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
