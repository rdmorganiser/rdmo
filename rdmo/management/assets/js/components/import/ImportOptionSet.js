import React, { Component } from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

import { ShowLink } from '../common/Links'

import Fields from './common/Fields'
import Form from './common/Form'

import { codeClass } from '../../constants/elements'

const ImportOptionSet = ({ config, optionset, importActions }) => {
  const showFields = () => importActions.updateElement(optionset, {show: !optionset.show})
  const toggleImport = () => importActions.updateElement(optionset, {import: !optionset.import})
  const updateOptionSet = (key, value) => importActions.updateElement(optionset, {key: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <ShowLink element={optionset} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label>
          <input type="checkbox" checked={optionset.import} onChange={toggleImport} />
          <strong>{gettext('Option set')}{' '}</strong>
          <code className={codeClass[optionset.type]}>{optionset.uri}</code>
        </label>
      </div>
      {
        optionset.show && <>
          <Form config={config} element={optionset} updateElement={updateOptionSet} />
          <Fields element={optionset} />
        </>
      }
    </li>
  )
}

ImportOptionSet.propTypes = {
  optionset: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportOptionSet