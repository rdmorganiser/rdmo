import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'

const Pending = ({ config }) => {
  if (config.pending) {
    return <i className="fa fa-circle-o-notch fa-spin fa-fw"></i>
  } else {
    return null
  }
}

Pending.propTypes = {
  config: PropTypes.object.isRequired,
}

function mapStateToProps(state) {
  return {
    config: state.config,
  }
}

export default connect(mapStateToProps)(Pending)
