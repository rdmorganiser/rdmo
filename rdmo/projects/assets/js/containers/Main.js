import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import isEmpty from 'lodash/isEmpty'
import * as projectActions from '../actions/projectsActions'
import Projects from '../components/main/Projects'

const Main = ({ projectActions, projects }) => {
    // check if anything was loaded yet
    if (!isEmpty(projects)) {
      return <Projects projects={projects} projectActions={projectActions} />
    }

    return null
}

Main.propTypes = {
  projectActions: PropTypes.object.isRequired,
  projects: PropTypes.object.isRequired,
}

function mapStateToProps(state) {
  return {
    projects: state.projects,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    projectActions: bindActionCreators(projectActions, dispatch),
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Main)
