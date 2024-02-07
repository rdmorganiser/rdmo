import React from 'react'
import PropTypes from 'prop-types'

import { AvailableLink, CodeLink, WarningLink, ErrorLink, ShowLink } from '../common/Links'

import Errors from './common/Errors'
import Fields from './common/Fields'
import Form from './common/Form'
import Warnings from './common/Warnings'

import { codeClass } from '../../constants/elements'

const ImportTask = ({ config, task, importActions }) => {
  const showFields = () => importActions.updateElement(task, {show: !task.show})
  const toggleImport = () => importActions.updateElement(task, {import: !task.import})
  const toggleAvailable = () => importActions.updateElement(task, {available: !task.available})
  const updateTask = (key, value) => importActions.updateElement(task, {[key]: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <AvailableLink element={task} verboseName={gettext('task')} onClick={toggleAvailable} />
        <WarningLink element={task} onClick={showFields} />
        <ErrorLink element={task} onClick={showFields} />
        <ShowLink element={task} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label className="mr-5">
          <input type="checkbox" checked={task.import} onChange={toggleImport} />
          <strong>{gettext('Task')}</strong>
        </label>
        <CodeLink className={codeClass[task.model]} uri={task.uri} onClick={showFields} />
      </div>
      {
        task.show && <>
          <Form config={config} element={task} updateElement={updateTask} />
          <Fields element={task} />
          <Warnings element={task} />
          <Errors element={task} />
        </>
      }
    </li>
  )
}

ImportTask.propTypes = {
  config: PropTypes.object.isRequired,
  task: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportTask
