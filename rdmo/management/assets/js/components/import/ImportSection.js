import React from 'react'
import PropTypes from 'prop-types'

import { CodeLink, WarningLink, ErrorLink, ShowLink } from '../common/Links'

import Errors from './common/Errors'
import Fields from './common/Fields'
import Form from './common/Form'
import Warnings from './common/Warnings'

import { codeClass } from '../../constants/elements'

const ImportSection = ({ config, section, importActions }) => {
  const showFields = () => importActions.updateElement(section, {show: !section.show})
  const toggleImport = () => importActions.updateElement(section, {import: !section.import})
  const updateSection = (key, value) => importActions.updateElement(section, {[key]: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <WarningLink element={section} onClick={showFields} />
        <ErrorLink element={section} onClick={showFields} />
        <ShowLink element={section} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label className="mr-5">
          <input type="checkbox" checked={section.import} onChange={toggleImport} />
          <strong>{gettext('Section')}</strong>
        </label>
        <CodeLink className={codeClass[section.model]} uri={section.uri} onClick={showFields} />
      </div>
      {
        section.show && <>
          <Form config={config} element={section} updateElement={updateSection} />
          <Fields element={section} />
          <Warnings element={section} />
          <Errors element={section} />
        </>
      }
    </li>
  )
}

ImportSection.propTypes = {
  config: PropTypes.object.isRequired,
  section: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportSection
