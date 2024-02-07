import React from 'react'
import PropTypes from 'prop-types'

import { CodeLink, WarningLink, ErrorLink, ShowLink } from '../common/Links'

import Errors from './common/Errors'
import Fields from './common/Fields'
import Form from './common/Form'
import Warnings from './common/Warnings'

import { codeClass } from '../../constants/elements'

const ImportOption = ({ config, option, importActions }) => {
  const showFields = () => importActions.updateElement(option, {show: !option.show})
  const toggleImport = () => importActions.updateElement(option, {import: !option.import})
  const updateOption = (key, value) => importActions.updateElement(option, {[key]: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <WarningLink element={option} onClick={showFields} />
        <ErrorLink element={option} onClick={showFields} />
        <ShowLink element={option} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label className="mr-5">
          <input type="checkbox" checked={option.import} onChange={toggleImport} />
          <strong>{gettext('Option')}</strong>
        </label>
        <CodeLink className={codeClass[option.model]} uri={option.uri} onClick={showFields} />
      </div>
      {
        option.show && <>
          <Form config={config} element={option} updateElement={updateOption} />
          <Fields element={option} />
          <Warnings element={option} />
          <Errors element={option} />
        </>
      }
    </li>
  )
}

ImportOption.propTypes = {
  config: PropTypes.object.isRequired,
  option: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportOption
