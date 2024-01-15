import React from 'react'
import PropTypes from 'prop-types'

import { CodeLink, WarningLink, ErrorLink, ShowLink } from '../common/Links'

import Errors from './common/Errors'
import Fields from './common/Fields'
import Form from './common/Form'
import Warnings from './common/Warnings'

import { codeClass, verboseNames } from '../../constants/elements'
import { isEmpty } from 'lodash'

const ImportElement = ({ config, instance, importActions }) => {
  const showFields = () => importActions.updateElement(instance, {show: !instance.show})
  const toggleImport = () => importActions.updateElement(instance, {import: !instance.import})
  const updateInstance = (key, value) => importActions.updateElement(instance, {[key]: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <WarningLink element={instance} onClick={showFields} />
        <ErrorLink element={instance} onClick={showFields} />
        <ShowLink element={instance} onClick={showFields} />
        {
          instance.updated && !isEmpty(instance.updated_and_changed) && !instance.created &&
          <p className="element-link fa fa-pencil"></p>
        }
      </div>
      <div className="checkbox">
        <label className="mr-5">
          <input type="checkbox" checked={instance.import} onChange={toggleImport} />
          <strong>{verboseNames[instance.model]}{' '}</strong>
        </label>
        <CodeLink className={codeClass[instance.model]} uri={instance.uri} onClick={showFields} />
      </div>
      {
        instance.show && <>
          <Form config={config} element={instance} updateElement={updateInstance} />
          <Fields element={instance} />
          <Warnings element={instance} />
          <Errors element={instance} />
        </>
      }
    </li>
  )
}

ImportElement.propTypes = {
  config: PropTypes.object.isRequired,
  instance: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportElement
