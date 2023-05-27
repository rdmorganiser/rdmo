import React from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'
import uniqueId from 'lodash/uniqueId'

const Errors = ({ element }) => {
  return !isEmpty(element.errors) && <div className="row text-danger mt-10">
    <div className="col-sm-3 text-right">
      {gettext('Errors')}
    </div>
    <div className="col-sm-9">
      <ul className="list-unstyled">
        {
          element.errors.map(message => <li key={uniqueId('error-')}>{message}</li>)
        }
      </ul>
    </div>
  </div>
}

Errors.propTypes = {
  element: PropTypes.object.isRequired
}

export default Errors
