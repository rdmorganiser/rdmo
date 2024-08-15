// WarningsListGroup.js
import React from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'
import { codeClass, verboseNames } from '../../../constants/elements'

// Helper function to generate warning messages
export const generateWarningListItems = (elementWarnings, elementModel, shouldShowURI = true) =>
  Object.entries(elementWarnings).flatMap(([uri, messages]) =>
    messages.map(message => (
      <li className="list-group-item" key={uniqueId('warning-uri-message')}>
        {shouldShowURI && (
          <>
            <strong>{verboseNames[elementModel]}{' '}</strong>
            <code className={codeClass[elementModel]}>{uri}</code>
            <br />
          </>
        )}
        <div className="text-warning">
          {message}
        </div>
      </li>
    ))
  )

const WarningsListGroup = ({ elementWarnings, elementModel, shouldShowURI }) => {
  return (
    <ul className="list-group">
      {generateWarningListItems(elementWarnings, elementModel, shouldShowURI)}
    </ul>
  )
}

WarningsListGroup.propTypes = {
  elementWarnings: PropTypes.object.isRequired,
  elementModel: PropTypes.string.isRequired,
  shouldShowURI: PropTypes.bool
}

export default WarningsListGroup
