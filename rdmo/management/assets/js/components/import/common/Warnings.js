import React from 'react'
import PropTypes from 'prop-types'
// import isEmpty from 'lodash/isEmpty'
import uniqueId from 'lodash/uniqueId'
import {codeClass} from '../../../constants/elements'

const Warnings = ({element, success = false}) => {
  const listWarningMessages = Object.entries(element.warnings).map(([uri, messages]) => {
    return (
      <li key={uniqueId('warning-uri-')}><code className={codeClass['domain.attribute']}>{uri}</code>
        <ul className="list-unstyled">
          {
            messages.map(message => {
              return (
                <li className="text-warning" key={uniqueId('warning-uri-message')}>{message}</li>
              )
            })
          }
        </ul>
      </li>
    )
  })

  return (
    <div className="row text-warning mt-10">
      {
        success === true && listWarningMessages.length > 0 &&
        <div className="col-sm-3 text-right">
          {gettext('Warnings')}
        </div>
      }
      <div className="col-sm-9">
        <ul className="list-unstyled">{listWarningMessages}</ul>
      </div>
    </div>
  )
}

Warnings.propTypes = {
  element: PropTypes.object.isRequired,
  success: PropTypes.bool.isRequired
}

export default Warnings
