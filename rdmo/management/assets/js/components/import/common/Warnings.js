import React from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'
import uniqueId from 'lodash/uniqueId'
import {codeClass} from '../../../constants/elements'

const Warnings = ({ element, success = false }) => {
  return !isEmpty(element.warnings) && <div className="row mt-10">
    { (success === true) &&
    <div className="col-sm-3 text-warning text-right">
      {gettext('Warnings')}
    </div>
  }
    <div className="col-sm-9">
      <ul className="list-unstyled">
        {
          Object.entries(element.warnings).map(([uri, messages]) => {
              return (
                  <li key={uniqueId('warning-uri-')}><code className={codeClass['domain.attribute']}>{uri}</code>
                    <div className="col-sm-9">
                      <ul className="list-unstyled">
                        {
                          messages.map(message => (
                              <li className="text-warning" key={uniqueId('warning-uri-message')}>{message}</li>))
                        }
                      </ul>
                    </div>
                  </li>
              )
          })
        }
      </ul>
    </div>
  </div>
}

Warnings.propTypes = {
  element: PropTypes.object.isRequired,
  success: PropTypes.bool.isRequired
}

export default Warnings
