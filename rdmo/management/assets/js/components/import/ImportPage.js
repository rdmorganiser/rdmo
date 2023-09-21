import React from 'react'
import PropTypes from 'prop-types'

import { CodeLink, WarningLink, ErrorLink, ShowLink } from '../common/Links'

import Errors from './common/Errors'
import Fields from './common/Fields'
import Form from './common/Form'
import Warnings from './common/Warnings'

import { codeClass } from '../../constants/elements'

const ImportPage = ({ config, page, importActions }) => {
  const showFields = () => importActions.updateElement(page, {show: !page.show})
  const toggleImport = () => importActions.updateElement(page, {import: !page.import})
  const updatePage = (key, value) => importActions.updateElement(page, {[key]: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <WarningLink element={page} onClick={showFields} />
        <ErrorLink element={page} onClick={showFields} />
        <ShowLink element={page} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label className="mr-5">
          <input type="checkbox" checked={page.import} onChange={toggleImport} />
          <strong>{gettext('Page')}</strong>
        </label>
        <CodeLink className={codeClass[page.model]} uri={page.uri} onClick={showFields} />
      </div>
      {
        page.show && <>
          <Form config={config} element={page} updateElement={updatePage} />
          <Fields element={page} />
          <Warnings element={page} />
          <Errors element={page} />
        </>
      }
    </li>
  )
}

ImportPage.propTypes = {
  config: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportPage
