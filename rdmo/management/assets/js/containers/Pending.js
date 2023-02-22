import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'

class Pending extends Component {

  constructor(props) {
    super(props)
  }

  render() {
    const { config } = this.props

    if (config.pending) {
      return <i className="fa fa-circle-o-notch fa-spin fa-fw"></i>
    } else {
      return null
    }
  }
}

Pending.propTypes = {
  config: PropTypes.object.isRequired,
}

function mapStateToProps(state, props) {
  return {
    config: state.config,
  }
}

export default connect(mapStateToProps)(Pending)
