import React from 'react'
import PropTypes from 'prop-types'

import { CodeLink, WarningLink, ErrorLink, ShowLink } from '../common/Links'

import Errors from './common/Errors'
import Fields from './common/Fields'
import Form from './common/Form'
import Warnings from './common/Warnings'

import { codeClass } from '../../constants/elements'

const ImportOptionSet = ({ config, optionset, importActions }) => {
  const showFields = () => importActions.updateElement(optionset, {show: !optionset.show})
  const toggleImport = () => importActions.updateElement(optionset, {import: !optionset.import})
  const updateOptionSet = (key, value) => importActions.updateElement(optionset, {[key]: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <WarningLink element={optionset} onClick={showFields} />
        <ErrorLink element={optionset} onClick={showFields} />
        <ShowLink element={optionset} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label className="mr-5">
          <input type="checkbox" checked={optionset.import} onChange={toggleImport} />
          <strong>{gettext('Option set')}</strong>
        </label>
        <CodeLink className={codeClass[optionset.model]} uri={optionset.uri} onClick={showFields} />
      </div>
      {
        optionset.show && <>
          <Form config={config} element={optionset} updateElement={updateOptionSet} />
          <Fields element={optionset} />
          <Warnings element={optionset} />
          <Errors element={optionset} />
        </>
      }
    </li>
  )
}

ImportOptionSet.propTypes = {
  config: PropTypes.object.isRequired,
  optionset: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportOptionSet
