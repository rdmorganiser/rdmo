import React, { Component } from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

import { ShowLink } from '../common/Links'

import Fields from './common/Fields'
import Form from './common/Form'

import { codeClass } from '../../constants/elements'

const ImportSection = ({ config, section, importActions }) => {
  const showFields = () => importActions.updateElement(section, {show: !section.show})
  const toggleImport = () => importActions.updateElement(section, {import: !section.import})
  const updateSection = (key, value) => importActions.updateElement(section, {key: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <ShowLink element={section} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label>
          <input type="checkbox" checked={section.import} onChange={toggleImport} />
          <strong>{gettext('Section')}{' '}</strong>
          <code className={codeClass[section.type]}>{section.uri}</code>
        </label>
      </div>
      {
        section.show && <>
          <Form config={config} element={section} updateElement={updateSection} />
          <Fields element={section} />
        </>
      }
    </li>
  )
}

ImportSection.propTypes = {
  section: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportSection