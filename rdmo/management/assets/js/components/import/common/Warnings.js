import React from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

import {codeClass} from '../../../constants/elements'


const Warnings = ({element, showTitle = false, shouldShowURI = true}) => {
  const generateWarningMessagesForUri = (messages, key) =>
    messages.map(message => <li className="text-warning" key={key}>{message}</li>)

  const prepareWarningsList = (warningsObj) =>
    Object.entries(warningsObj).map(([uri, messages]) => (
      <ul className="list-unstyled" key={uniqueId('warning-uri-list')}>
        {shouldShowURI &&
          <li key={uniqueId('warning-uri-')}>
            <code className={codeClass['domain.attribute']}>{uri}</code>
          </li>
        }
        {generateWarningMessagesForUri(messages, uniqueId('warning-uri-message'))}
      </ul>
    ))

  const listWarningMessages = prepareWarningsList(element.warnings)

  return (
    <div className="row text-warning mt-10">
      {showTitle === true && listWarningMessages.length > 0 &&
        <div className="col-sm-3 mb-5 mt-5">
          {'Warnings'}
        </div>
      }
      <div className="col-sm-12">
        {listWarningMessages}
      </div>
    </div>
  )
}


Warnings.propTypes = {
    element: PropTypes.object.isRequired,
    showTitle: PropTypes.bool.isRequired,
    shouldShowURI: PropTypes.bool,
  }

  export default Warnings
