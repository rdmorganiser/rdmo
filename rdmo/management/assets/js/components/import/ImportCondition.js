import React from 'react'
import PropTypes from 'prop-types'

import { CodeLink, WarningLink, ErrorLink, ShowLink } from '../common/Links'

import Errors from './common/Errors'
import Fields from './common/Fields'
import Form from './common/Form'
import Warnings from './common/Warnings'

import { codeClass } from '../../constants/elements'

const ImportCondition = ({ config, condition, importActions }) => {
  const showFields = () => importActions.updateElement(condition, {show: !condition.show})
  const toggleImport = () => importActions.updateElement(condition, {import: !condition.import})
  const updateCondition = (key, value) => importActions.updateElement(condition, {[key]: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <WarningLink element={condition} onClick={showFields} />
        <ErrorLink element={condition} onClick={showFields} />
        <ShowLink element={condition} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label className="mr-5">
          <input type="checkbox" checked={condition.import} onChange={toggleImport} />
          <strong>{gettext('Condition')}</strong>
        </label>
        <CodeLink className={codeClass[condition.model]} uri={condition.uri} onClick={showFields} />
      </div>
      {
        condition.show && <>
          <Form config={config} element={condition} updateElement={updateCondition} />
          <Fields element={condition} />
          <Warnings element={condition} />
          <Errors element={condition} />
        </>
      }
    </li>
  )
}

ImportCondition.propTypes = {
  config: PropTypes.object.isRequired,
  condition: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportCondition
