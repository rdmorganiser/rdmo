import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { codeClassNames } from '../../constants/elements'

const ElementHeading = ({ verboseName, element, onSave }) => {
  return (
    <div className="panel-heading">
      <div className="pull-right">
        <button className="btn btn-xs btn-default" onClick={event => history.back()}>
          {gettext('Back')}
        </button>
        {' '}
        <button className="btn btn-xs btn-primary" onClick={event => onSave()}>
          {gettext('Save')}
        </button>
      </div>
      <div>
        <strong>{verboseName}{': '}</strong>
        <code className={codeClassNames[element.type]}>{element.uri}</code>
      </div>
    </div>
  )
}

ElementHeading.propTypes = {
  verboseName: PropTypes.string.isRequired,
  element: PropTypes.object.isRequired,
  onSave: PropTypes.func.isRequired
}

export default ElementHeading
