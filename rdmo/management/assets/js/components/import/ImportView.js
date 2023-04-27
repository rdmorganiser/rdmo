import React, { Component } from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

import { ShowLink } from '../common/Links'

import Fields from './common/Fields'
import Form from './common/Form'

import { codeClass } from '../../constants/elements'

const ImportView = ({ config, view, importActions }) => {
  const showFields = () => importActions.updateElement(view, {show: !view.show})
  const toggleImport = () => importActions.updateElement(view, {import: !view.import})
  const updateView = (key, value) => importActions.updateElement(view, {key: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <ShowLink element={view} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label>
          <input type="checkbox" checked={view.import} onChange={toggleImport} />
          <strong>{gettext('View')}{' '}</strong>
          <code className={codeClass[view.type]}>{view.uri}</code>
        </label>
      </div>
      {
        view.show && <>
          <Form config={config} element={view} updateElement={updateView} />
          <Fields element={view} />
        </>
      }
    </li>
  )
}

ImportView.propTypes = {
  view: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportView