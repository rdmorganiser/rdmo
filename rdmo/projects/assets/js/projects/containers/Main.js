import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import * as userActions from 'rdmo/core/assets/js/actions/userActions'

import * as projectsActions from '../actions/projectsActions'

import Projects from '../components/main/Projects'

const Main = ({ config, configActions, projectsActions, projects, userActions, currentUser }) => {
  if (projects.ready) {
      return (
        <Projects
          config={config}
          configActions={configActions}
          currentUserObject={currentUser}
          projectsActions={projectsActions}
          projectsObject={projects}
          userActions={userActions}
        />
      )
    }

    return null
}

Main.propTypes = {
  config: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  currentUser: PropTypes.object.isRequired,
  projectsActions: PropTypes.object.isRequired,
  projects: PropTypes.object.isRequired,
  userActions: PropTypes.object.isRequired
}

function mapStateToProps(state) {
  return {
    config: state.config,
    currentUser: state.currentUser,
    projects: state.projects,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    configActions: bindActionCreators(configActions, dispatch),
    projectsActions: bindActionCreators(projectsActions, dispatch),
    userActions: bindActionCreators(userActions, dispatch),
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Main)
