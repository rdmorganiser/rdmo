import React from 'react'
import PropTypes from 'prop-types'

import { CodeLink, WarningLink, ErrorLink, ShowLink, ShowUpdatedLink } from '../common/Links'

import Errors from './common/Errors'
import Fields from './common/Fields'
import Form from './common/Form'

import { codeClass, verboseNames } from '../../constants/elements'
import { isEmpty } from 'lodash'

const ImportElement = ({ config, element, importActions }) => {
  const updateShowField = () => importActions.updateElement(element, {show: !element.show})
  const toggleImport = () => importActions.updateElement(element, {import: !element.import})
  const updateElement = (key, value) => importActions.updateElement(element, {[key]: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <WarningLink show={!isEmpty(element.warnings)} onClick={updateShowField} />
        <ErrorLink show={!isEmpty(element.errors)} onClick={updateShowField} />
        <ShowUpdatedLink show={(element.changed && !element.created)} disabled={true} onClick={updateShowField} />
        <ShowLink show={element.show} onClick={updateShowField} />

      </div>
      <div className="checkbox">
        <label className="mr-5">
          <input type="checkbox" checked={element.import} onChange={toggleImport} />
          <strong>{verboseNames[element.model]}{' '}</strong>
        </label>
        <CodeLink className={codeClass[element.model]} uri={element.uri} onClick={updateShowField} />
      </div>
      {
        element.show && <>
          <Form config={config} element={element} updateElement={updateElement} />
          <Fields element={element} />
          <Errors element={element} />
        </>
      }
    </li>
  )
}

ImportElement.propTypes = {
  config: PropTypes.object.isRequired,
  element: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportElement
