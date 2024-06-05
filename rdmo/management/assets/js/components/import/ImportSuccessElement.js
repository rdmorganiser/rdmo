import React from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

import { codeClass, verboseNames } from '../../constants/elements'
import { isEmpty } from 'lodash'
import Warnings from './common/Warnings'
import { ShowUpdatedLink } from '../common/Links'

const prepareErrorsList = (errors) => {
  // Filter out duplicate errors
  const uniqueErrors = [...new Set(errors)]

  return uniqueErrors.map(message => (
    <p key={uniqueId()} className="text-danger">{message}</p>
  ))
}

const ImportSuccessElement = ({ element, importActions }) => {
  const listErrorMessages = prepareErrorsList(element.errors)

  const updateShowField = () => importActions.updateElement(element, { show: !element.show })

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <Warnings element={element} showTitle={true} />
      </div>
      <div>
        <strong>{verboseNames[element.model]}{' '}</strong>
        <code className={codeClass[element.model]}>{element.uri}</code>
        {element.created && (
          <>
            <span className="text-success">{' '}{gettext('created')} </span>
            <span className="muted element-link fa fa-plus"></span>
          </>
        )}
        {element.updated && (
          <ShowUpdatedLink show={(element.changed && !element.created)} disabled={true} onClick={updateShowField} />
        )}
        {!isEmpty(element.errors) && !(element.created || element.updated) && (
          <span className="text-danger">{' '}{gettext('could not be imported')}</span>
        )}
        {!isEmpty(element.errors) && (element.created || element.updated) && (
          <>
            {', '}
            <span className="text-danger">{gettext('but could not be added to parent element')}</span>
          </>
        )}
        {'.'}
      </div>
      {listErrorMessages}
    </li>
  )
}

ImportSuccessElement.propTypes = {
  element: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportSuccessElement
