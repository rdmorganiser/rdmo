import React from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'


const Diffs = ({ element }) => {
  return !isEmpty(element.difftables) && <div className="row text-danger mt-10">
    <div className="col-sm-3 text-right">
      {gettext('Diffs')}
    </div>
    <div className="col-sm-9">
    {
      element.difftables
    }
    </div>
  </div>
}

Diffs.propTypes = {
  element: PropTypes.object.isRequired
}

export default Diffs
