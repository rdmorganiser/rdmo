import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import * as projectActions from '../actions/projectActions'

const Main = ({ config, settings, templates, user, project, configActions, projectActions }) => {
  console.log(config, settings, templates, user, project)
  console.log(configActions, projectActions)

  return project && (
    <span>👍</span>
  )
}

Main.propTypes = {
    config: PropTypes.object.isRequired,
    settings: PropTypes.object.isRequired,
    templates: PropTypes.object.isRequired,
    user: PropTypes.object.isRequired,
    project: PropTypes.object.isRequired,
    configActions: PropTypes.object.isRequired,
    projectActions: PropTypes.object.isRequired
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
