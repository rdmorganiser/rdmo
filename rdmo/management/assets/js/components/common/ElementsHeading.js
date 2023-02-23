import React, { Component} from 'react'
import PropTypes from 'prop-types'

const ElementsHeading = ({ verboseName }) => {
  return (
    <div className="panel-heading">
      <div className="pull-right">
        <button className="btn btn-xs btn-default" onClick={event => history.back()}>
          {gettext('Back')}
        </button>
      </div>
      <div>
        <strong>{verboseName}</strong>
      </div>
    </div>
  )
}

ElementsHeading.propTypes = {
  verboseName: PropTypes.string.isRequired
}

export default ElementsHeading
