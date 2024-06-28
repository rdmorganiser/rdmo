import React from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'
import {codeClass, verboseNames} from '../../../constants/elements'


const Warnings = ({element, showTitle = false, shouldShowURI = true}) => {
  const warningListItems = (messages, uri) =>
    messages.map(message => (
      <li className="warning-item pb-5" key={uniqueId('warning-uri-message')}>
        {shouldShowURI && (
          <>
            <strong>{verboseNames[element.model]}{' '}</strong>
            <code className={codeClass[element.model]}>{uri}</code>
            <br/>
          </>
        )}
        <div className="text-warning">
           {message}
        </div>
      </li>
    ))

  const prepareWarningsList = (warningsObj) =>
    Object.entries(warningsObj).map(([uri, messages]) => (
      <ul className="list-unstyled warning-list" key={uniqueId('warning-uri-list')}>
        {warningListItems(messages, uri)}
      </ul>
    ))

  const warningsMessagesList = prepareWarningsList(element.warnings)
  const show =  warningsMessagesList.length > 0

  return show && (
    <div>
      {showTitle === true &&
        <div className="mb-5 mt-5 text-warning">
          {'Warnings'}
        </div>
      }
      <div className="mb-5 mt-5">
        {warningsMessagesList}
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
