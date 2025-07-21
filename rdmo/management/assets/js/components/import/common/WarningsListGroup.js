// WarningsListGroup.js
import React from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'
import { codeClass, verboseNames } from '../../../constants/elements'

// Helper function to generate warning messages
export const generateWarningListItems = (elementWarnings, elementModel, elementURI, shouldShowURI = true) =>
  Object.values(elementWarnings).flatMap((messages) =>
    messages.map(message => (
      <li className="list-group-item" key={uniqueId('warning-uri-message')}>
        {shouldShowURI && elementModel && elementURI && (
          <>
            <strong>{verboseNames[elementModel]}{' '}</strong>
            <code className={codeClass[elementModel]}>{elementURI}</code>
            <br />
          </>
        )}
        <div className="text-warning">
          {message}
        </div>
      </li>
    ))
  )

const WarningsListGroup = ({ elementWarnings, elementModel, elementURI, shouldShowURI }) => {
  return (
    <ul className="list-group">
      {generateWarningListItems(elementWarnings, elementModel, elementURI, shouldShowURI)}
    </ul>
  )
}

WarningsListGroup.propTypes = {
  elementWarnings: PropTypes.object.isRequired,
  elementModel: PropTypes.string.isRequired,
  elementURI: PropTypes.string.isRequired,
  shouldShowURI: PropTypes.bool
}

export default WarningsListGroup
