import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import * as projectActions from '../actions/projectActions'

import ProjectNavigation from '../components/main/ProjectNavigation'

const Main = ({ project }) => {
  return project.project && <ProjectNavigation />
}

Main.propTypes = {
    project: PropTypes.object.isRequired,
}

function mapStateToProps(state) {
  return {
    config: state.config,
    settings: state.settings,
    templates: state.templates,
    user: state.user,
    project: state.project
  }
}

function mapDispatchToProps(dispatch) {
  return {
    configActions: bindActionCreators(configActions, dispatch),
    projectActions: bindActionCreators(projectActions, dispatch)
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Main)
