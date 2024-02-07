import React from 'react'
import PropTypes from 'prop-types'

import { AvailableLink, CodeLink, WarningLink, ErrorLink, ShowLink } from '../common/Links'

import Errors from './common/Errors'
import Fields from './common/Fields'
import Form from './common/Form'
import Warnings from './common/Warnings'

import { codeClass } from '../../constants/elements'

const ImportCatalog = ({ config, catalog, importActions }) => {
  const showFields = () => importActions.updateElement(catalog, {show: !catalog.show})
  const toggleImport = () => importActions.updateElement(catalog, {import: !catalog.import})
  const toggleAvailable = () => importActions.updateElement(catalog, {available: !catalog.available})
  const updateCatalog = (key, value) => importActions.updateElement(catalog, {[key]: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <AvailableLink element={catalog} verboseName={gettext('catalog')} onClick={toggleAvailable} />
        <WarningLink element={catalog} onClick={showFields} />
        <ErrorLink element={catalog} onClick={showFields} />
        <ShowLink element={catalog} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label className="mr-5">
          <input type="checkbox" checked={catalog.import} onChange={toggleImport} />
          <strong>{gettext('Catalog')}</strong>
        </label>
        <CodeLink className={codeClass[catalog.model]} uri={catalog.uri} onClick={showFields} />
      </div>
      {
        catalog.show && <>
          <Form config={config} element={catalog} updateElement={updateCatalog} />
          <Fields element={catalog} />
          <Warnings element={catalog} />
          <Errors element={catalog} />
        </>
      }
    </li>
  )
}

ImportCatalog.propTypes = {
  config: PropTypes.object.isRequired,
  catalog: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportCatalog
