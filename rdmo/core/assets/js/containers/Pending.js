import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { isEmpty } from 'lodash'

const Pending = ({ pending }) => {
  return (
    !isEmpty(pending.items) && (
      <i className="fa fa-circle-o-notch fa-spin fa-fw"></i>
    )
  )
}

Pending.propTypes = {
  pending: PropTypes.object.isRequired,
}

function mapStateToProps(state) {
  return {
    pending: state.pending,
  }
}

export default connect(mapStateToProps)(Pending)
