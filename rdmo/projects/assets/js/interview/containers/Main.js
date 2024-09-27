import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import { hasErrors, isReady } from '../utils/interview'

import Breadcrump from '../components/main/Breadcrump'
import Contact from '../components/main/Contact'
import Done from '../components/main/Done'
import Page from '../components/main/page/Page'
import Errors from '../components/main/Errors'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'

import * as contactActions from '../actions/contactActions'
import * as interviewActions from '../actions/interviewActions'

const Main = ({ config, settings, templates, project, interview, contact,
                interviewActions, contactActions }) => {

  if (hasErrors(project, interview)) {
    return (
      <Errors
        templates={templates}
        errors={[...project.errors, ...interview.errors]}
      />
    )
  } else if (isReady(interview)) {
    return (
      <div>
        <Breadcrump
          overview={project.overview}
          page={interview.page}
          fetchPage={interviewActions.fetchPage}
        />
        {
          interview.done && (
            <Done templates={templates} />
          )
        }
        {
          interview.page && (
            <Page
              config={config}
              settings={settings}
              templates={templates}
              overview={project.overview}
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
              copyValue={interviewActions.copyValue}
              copySet={interviewActions.copySet}
              fetchContact={contactActions.fetchContact}
            />
          )
        }
        <Contact
          templates={templates}
          contact={contact}
          sendContact={contactActions.sendContact}
          closeContact={contactActions.closeContact}
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
  project: PropTypes.object.isRequired,
  interview: PropTypes.object.isRequired,
  contact: PropTypes.object.isRequired,
  interviewActions: PropTypes.object.isRequired,
  contactActions: PropTypes.object.isRequired
}

function mapStateToProps(state) {
  return {
    config: state.config,
    settings: state.settings,
    templates: state.templates,
    user: state.user,
    project: state.project,
    interview: state.interview,
    contact: state.contact,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    configActions: bindActionCreators(configActions, dispatch),
    interviewActions: bindActionCreators(interviewActions, dispatch),
    contactActions: bindActionCreators(contactActions, dispatch),
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Main)
