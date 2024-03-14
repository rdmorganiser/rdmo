import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import * as configActions from '../actions/configActions'

const Sidebar = ({ config, configActions }) => {

  console.log(config)
  console.log(configActions)

  // fetching the data is not complete yet, or no action was invoked yet
  return (
    <div>
      Sidebar
    </div>
  )
}

Sidebar.propTypes = {
  config: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired
}

function mapStateToProps(state) {
  return {
    config: state.config
  }
}

function mapDispatchToProps(dispatch) {
  return {
    configActions: bindActionCreators(configActions, dispatch)
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Sidebar)
