import React, { Component } from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

import { CodeLink, ShowLink } from '../common/Links'

import Fields from './common/Fields'
import Form from './common/Form'

import { codeClass } from '../../constants/elements'

const ImportCondition = ({ config, condition, importActions }) => {
  const showFields = () => importActions.updateElement(condition, {show: !condition.show})
  const toggleImport = () => importActions.updateElement(condition, {import: !condition.import})
  const updateCondition = (key, value) => importActions.updateElement(condition, {key: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <ShowLink element={condition} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label className="mr-5">
          <input type="checkbox" checked={condition.import} onChange={toggleImport} />
          <strong>{gettext('Condition')}</strong>
        </label>
        <CodeLink className={codeClass[condition.type]} uri={condition.uri} onClick={showFields} />
      </div>
      {
        condition.show && <>
          <Form config={config} element={condition} updateElement={updateCondition} />
          <Fields element={condition} />
        </>
      }
    </li>
  )
}

ImportCondition.propTypes = {
  condition: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportCondition