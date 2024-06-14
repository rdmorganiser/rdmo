import React from 'react'
import PropTypes from 'prop-types'

import { codeClass, verboseNames } from '../../constants/elements'
import { isEmpty } from 'lodash'
import Warnings from './common/Warnings'
import {prepareErrorsList } from './common/Errors'
import {EditLink} from '../common/Links'



const ImportSuccessElement = ({ element, importActions }) => {
  const listErrorMessages = prepareErrorsList(element.errors)

  const updateShowField = () => importActions.updateElement(element, { show: !element.show })

  return (
    <li className="list-group-item">
      <div>
        <strong>{verboseNames[element.model]}{' '}</strong>
        <code className={codeClass[element.model]}>{element.uri}</code>
        {element.created && (
          <>
            <span className="text-success">{' '}{gettext('created')} </span>
            <span className="muted element-link fa fa-plus"></span>
          </>
        )}
        {element.updated && element.changed && (
          <EditLink href={''} title={gettext('Updated')} disabled={true} onClick={updateShowField} />
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
      <Warnings element={element} showTitle={true} shouldShowURI={false} />
      {listErrorMessages}
    </li>
  )
}

ImportSuccessElement.propTypes = {
  element: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportSuccessElement
