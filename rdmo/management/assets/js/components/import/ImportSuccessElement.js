import React from 'react'
import PropTypes from 'prop-types'
import { isEmpty } from 'lodash'

import { codeClass, verboseNames } from '../../constants/elements'
import Warnings from './common/Warnings'
import Errors from './common/Errors'

const ImportSuccessElement = ({ element, importActions }) => {

  const updateShowField = () => importActions.updateElement(element, { show: !element.show })

  return (
    <li className="list-group-item">
      <div className="mb-5">
        <strong>{verboseNames[element.model]}{' '}</strong>
        <code className={codeClass[element.model]}>{element.uri}</code>
        {element.updated && element.changed && (
        <span className="label label-info ml-5" onClick={updateShowField}>
          {gettext('changed')}</span>
        )}
        {element.created && (
          <span className="label label-success ml-5" onClick={updateShowField}>
            {gettext('created')}</span>
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
      </div>
      <Errors elementErrors={element.errors} />
      <Warnings elementWarnings={element.warnings} elementModel={element.model} showTitle={true} shouldShowURI={false} />
    </li>
  )
}

ImportSuccessElement.propTypes = {
  element: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportSuccessElement
