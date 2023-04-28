import React, { Component } from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

import { AvailableLink, CodeLink, ShowLink } from '../common/Links'

import Fields from './common/Fields'
import Form from './common/Form'

import { codeClass } from '../../constants/elements'

const ImportCatalog = ({ config, catalog, importActions }) => {
  const showFields = () => importActions.updateElement(catalog, {show: !catalog.show})
  const toggleImport = () => importActions.updateElement(catalog, {import: !catalog.import})
  const toggleAvailable = () => importActions.updateElement(catalog, {available: !catalog.available})
  const updateCatalog = (key, value) => importActions.updateElement(catalog, {key: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <AvailableLink element={catalog} verboseName={gettext('catalog')} onClick={toggleAvailable} />
        <ShowLink element={catalog} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label className="mr-5">
          <input type="checkbox" checked={catalog.import} onChange={toggleImport} />
          <strong>{gettext('Catalog')}</strong>
        </label>
        <CodeLink className={codeClass[catalog.type]} uri={catalog.uri} onClick={showFields} />
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
