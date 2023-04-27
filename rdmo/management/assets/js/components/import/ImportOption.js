import React, { Component } from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

import { ShowLink } from '../common/Links'

import Fields from './common/Fields'
import Form from './common/Form'

import { codeClass } from '../../constants/elements'

const ImportOption = ({ config, option, importActions }) => {
  const showFields = () => importActions.updateElement(option, {show: !option.show})
  const toggleImport = () => importActions.updateElement(option, {import: !option.import})
  const updateOption = (key, value) => importActions.updateElement(option, {key: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <ShowLink element={option} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label>
          <input type="checkbox" checked={option.import} onChange={toggleImport} />
          <strong>{gettext('Option')}{' '}</strong>
          <code className={codeClass[option.type]}>{option.uri}</code>
        </label>
      </div>
      {
        option.show && <>
          <Form config={config} element={option} updateElement={updateOption} />
          <Fields element={option} />
        </>
      }
    </li>
  )
}

ImportOption.propTypes = {
  option: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportOption