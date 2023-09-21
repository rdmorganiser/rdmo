import React from 'react'
import PropTypes from 'prop-types'

import { AvailableLink, CodeLink, WarningLink, ErrorLink, ShowLink } from '../common/Links'

import Errors from './common/Errors'
import Fields from './common/Fields'
import Form from './common/Form'
import Warnings from './common/Warnings'

import { codeClass } from '../../constants/elements'

const ImportView = ({ config, view, importActions }) => {
  const showFields = () => importActions.updateElement(view, {show: !view.show})
  const toggleImport = () => importActions.updateElement(view, {import: !view.import})
  const toggleAvailable = () => importActions.updateElement(view, {available: !view.available})
  const updateView = (key, value) => importActions.updateElement(view, {[key]: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <AvailableLink element={view} verboseName={gettext('view')} onClick={toggleAvailable} />
        <WarningLink element={view} onClick={showFields} />
        <ErrorLink element={view} onClick={showFields} />
        <ShowLink element={view} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label className="mr-5">
          <input type="checkbox" checked={view.import} onChange={toggleImport} />
          <strong>{gettext('View')}</strong>
        </label>
        <CodeLink className={codeClass[view.model]} uri={view.uri} onClick={showFields} />
      </div>
      {
        view.show && <>
          <Form config={config} element={view} updateElement={updateView} />
          <Fields element={view} />
          <Warnings element={view} />
          <Errors element={view} />
        </>
      }
    </li>
  )
}

ImportView.propTypes = {
  config: PropTypes.object.isRequired,
  view: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportView
