import React from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'
import uniqueId from 'lodash/uniqueId'

const Warnings = ({ element }) => {
  return !isEmpty(element.warnings) && <div className="row text-warning mt-10">
    <div className="col-sm-3 text-right">
      {gettext('Warnings')}
    </div>
    <div className="col-sm-9">
      <ul className="list-unstyled">
        {
          element.warnings.map(message => <li key={uniqueId('error-')}>{message}</li>)
        }
      </ul>
    </div>
  </div>
}

Warnings.propTypes = {
  element: PropTypes.object.isRequired
}

export default Warnings
