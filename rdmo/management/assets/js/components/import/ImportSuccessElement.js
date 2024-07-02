import React from 'react'
import PropTypes from 'prop-types'
import { isEmpty } from 'lodash'

import { codeClass, verboseNames } from '../../constants/elements'
import Warnings from './common/Warnings'
import Errors from './common/Errors'
import {ChangedLabel, CreatedLabel} from './common/ImportLabels'



const ImportSuccessElement = ({ element, importActions }) => {

  const updateShowField = () => importActions.updateElement(element, { show: !element.show })

  return (
    <li className="list-group-item">
      <div className="mb-5">
        <strong>{verboseNames[element.model]}{' '}</strong>
        <code className={codeClass[element.model]}>{element.uri}</code>
        <CreatedLabel onClick={updateShowField} show={element.created} />

        <ChangedLabel onClick={updateShowField} show={(element.changed && element.updated)} />

        {
          !isEmpty(element.errors) && !(element.created || element.updated) && (
          <span className="text-danger">{' '}{gettext('could not be imported')}</span>
        )}
        {
          !isEmpty(element.errors) && (element.created || element.updated) && (
          <>
            {', '}
            <span className="text-danger">{gettext('but could not be added to parent element')}</span>
          </>
        )}
        {'.'}
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
