import React from 'react'
import PropTypes from 'prop-types'

import { CodeLink, WarningLink, ErrorLink, ShowLink } from '../common/Links'

import Errors from './common/Errors'
import Fields from './common/Fields'
import Form from './common/Form'
import Warnings from './common/Warnings'

import { codeClass } from '../../constants/elements'

const ImportAttribute = ({ config, attribute, importActions }) => {
  const showFields = () => importActions.updateElement(attribute, {show: !attribute.show})
  const toggleImport = () => importActions.updateElement(attribute, {import: !attribute.import})
  const updateAttribute = (key, value) => importActions.updateElement(attribute, {[key]: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <WarningLink element={attribute} onClick={showFields} />
        <ErrorLink element={attribute} onClick={showFields} />
        <ShowLink element={attribute} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label className="mr-5">
          <input type="checkbox" checked={attribute.import} onChange={toggleImport} />
          <strong>{gettext('Attribute')}</strong>
        </label>
        <CodeLink className={codeClass[attribute.model]} uri={attribute.uri} onClick={showFields} />
      </div>
      {
        attribute.show && <>
          <Form config={config} element={attribute} updateElement={updateAttribute} />
          <Fields element={attribute} />
          <Warnings element={attribute} />
          <Errors element={attribute} />
        </>
      }
    </li>
  )
}

ImportAttribute.propTypes = {
  config: PropTypes.object.isRequired,
  attribute: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportAttribute
