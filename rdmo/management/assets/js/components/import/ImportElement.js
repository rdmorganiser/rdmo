import React from 'react'
import PropTypes from 'prop-types'

import { CodeLink, WarningLink, ErrorLink, ShowLink } from '../common/Links'

import Errors from './common/Errors'
import Fields from './common/Fields'
import Form from './common/Form'
import Warnings from './common/Warnings'

import { codeClass, verboseNames } from '../../constants/elements'
import { isEmpty } from 'lodash'

const ImportElement = ({ config, element, importActions }) => {
  const showFields = () => importActions.updateElement(element, {show: !element.show})
  const toggleImport = () => importActions.updateElement(element, {import: !element.import})
  const updateElement = (key, value) => importActions.updateElement(element, {[key]: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <WarningLink element={element} onClick={showFields} />
        <ErrorLink element={element} onClick={showFields} />
        <ShowLink element={element} onClick={showFields} />
        {
          element.updated && !isEmpty(element.updated_and_changed) && !element.created &&
          <p className="element-link fa fa-pencil"></p>
        }
      </div>
      <div className="checkbox">
        <label className="mr-5">
          <input type="checkbox" checked={element.import} onChange={toggleImport} />
          <strong>{verboseNames[element.model]}{' '}</strong>
        </label>
        <CodeLink className={codeClass[element.model]} uri={element.uri} onClick={showFields} />
      </div>
      {
        element.show && <>
          <Form config={config} element={element} updateElement={updateElement} />
          <Fields element={element} />
          <Warnings element={element} />
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
