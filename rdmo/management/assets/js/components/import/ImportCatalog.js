import React, { Component } from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

import { ShowLink } from '../common/Links'

import Fields from './common/Fields'
import Form from './common/Form'

import { codeClass } from '../../constants/elements'

const ImportCatalog = ({ config, catalog, importActions }) => {
  const showFields = () => importActions.updateElement(catalog, {show: !catalog.show})
  const toggleImport = () => importActions.updateElement(catalog, {import: !catalog.import})
  const updateCatalog = (key, value) => importActions.updateElement(section, {key: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <ShowLink element={catalog} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label>
          <input type="checkbox" checked={catalog.import} onChange={toggleImport} />
          <strong>{gettext('Catalog')}{' '}</strong>
          <code className={codeClass[catalog.type]}>{catalog.uri}</code>
        </label>
      </div>
      {
        catalog.show && <>
          <Form config={config} element={catalog} updateElement={updateCatalog} />
          <Fields element={catalog} />
        </>
      }
    </li>
  )
}

ImportCatalog.propTypes = {
  catalog: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportCatalog
