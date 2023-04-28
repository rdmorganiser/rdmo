import React, { Component } from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

import { CodeLink, ShowLink } from '../common/Links'

import Fields from './common/Fields'
import Form from './common/Form'

import { codeClass } from '../../constants/elements'

const ImportPage = ({ config, page, importActions }) => {
  const showFields = () => importActions.updateElement(page, {show: !page.show})
  const toggleImport = () => importActions.updateElement(page, {import: !page.import})
  const updatePage = (key, value) => importActions.updateElement(page, {key: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <ShowLink element={page} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label className="mr-5">
          <input type="checkbox" checked={page.import} onChange={toggleImport} />
          <strong>{gettext('Page')}</strong>
        </label>
        <CodeLink className={codeClass[page.type]} uri={page.uri} onClick={showFields} />
      </div>
      {
        page.show && <>
          <Form config={config} element={page} updateElement={updatePage} />
          <Fields element={page} />
        </>
      }
    </li>
  )
}

ImportPage.propTypes = {
  page: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportPage