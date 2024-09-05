import React from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap'
import get from 'lodash/get'

import Checkbox from './common/Checkbox'
import MultiSelect from './common/MultiSelect'
import Number from './common/Number'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'
import { ReadOnlyIcon } from '../common/Icons'

import TaskInfo from '../info/TaskInfo'
import DeleteTaskModal from '../modals/DeleteTaskModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditTask = ({ config, task, elements, elementActions}) => {

  const { sites, groups } = config
  const { elementAction, attributes, catalogs, conditions } = elements

  const updateTask = (key, value) => elementActions.updateElement(task, {[key]: value})
  const storeTask = (back) => elementActions.storeElement('tasks', task, elementAction, back)
  const deleteTask = () => elementActions.deleteElement('tasks', task)

  const editCondition = (condition) => elementActions.fetchElement('conditions', condition)
  const createCondition = () => elementActions.createElement('conditions', { task })

  const editAttribute = (attribute) => elementActions.fetchElement('attributes', attribute)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <TaskInfo task={task} elements={elements} />

  return (
    <div className="panel panel-default panel-edit">
      <div className="panel-heading">
        <div className="pull-right">
          <ReadOnlyIcon title={gettext('This task is read only')} show={task.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeTask} disabled={task.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeTask} disabled={task.read_only} back={true}/>
        </div>
        {
          task.id ? <>
            <strong>{gettext('Task')}{': '}</strong>
            <code className="code-tasks">{task.uri}</code>
          </> : <strong>{gettext('Create task')}</strong>
        }
      </div>

      {
        task.id && <div className="panel-body panel-border">
          { info }
        </div>
      }

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={task} field="uri_prefix"
                       onChange={updateTask} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={task} field="uri_path"
                  onChange={updateTask} />
          </div>
        </div>

        <Textarea config={config} element={task} field="comment"
                  rows={4} onChange={updateTask} />

        <div className="row">
          <div className="col-sm-4">
            <Checkbox config={config} element={task} field="locked"
                      onChange={updateTask} />
          </div>
          <div className="col-sm-4">
            <Checkbox config={config} element={task} field="available"
                      onChange={updateTask} />
          </div>
          <div className="col-sm-4">
            <Number config={config} element={task} field="order"
                    onChange={updateTask} />
          </div>
        </div>

        <Tabs id="#task-tabs" defaultActiveKey={0} animation={false}>
          {
            config.settings && config.settings.languages.map(([lang_code, lang], index) => (
              <Tab key={index} eventKey={index} title={lang}>
                <Text config={config} element={task} field={`title_${lang_code }`}
                      onChange={updateTask} />
                <Textarea config={config} element={task} field={`text_${lang_code }`}
                          rows={8} onChange={updateTask} />
              </Tab>
            ))
          }
        </Tabs>

        <MultiSelect config={config} element={task} field="conditions" options={conditions}
                     addText={gettext('Add existing condition')} createText={gettext('Create new condition')}
                     onChange={updateTask} onCreate={createCondition} onEdit={editCondition} />

        <Select config={config} element={task} field="start_attribute"
                options={attributes} onChange={updateTask} onEdit={editAttribute} />

        <Select config={config} element={task} field="end_attribute"
                options={attributes} onChange={updateTask} onEdit={editAttribute} />

        <div className="row">
          <div className="col-sm-6">
            <Number config={config} element={task} field="days_before"
                     onChange={updateTask} />
          </div>
          <div className="col-sm-6">
            <Number config={config} element={task} field="days_after"
                     onChange={updateTask} />
          </div>
        </div>

        <Select config={config} element={task} field="catalogs"
                options={catalogs} onChange={updateTask} isMulti />

        {get(config, 'settings.groups') && <Select config={config} element={task} field="groups"
                                                   options={groups} onChange={updateTask} isMulti />}

        {get(config, 'settings.multisite') && <Select config={config} element={task} field="sites"
                                                      options={sites} onChange={updateTask} isMulti />}

        {get(config, 'settings.multisite') && <Select config={config} element={task} field="editors"
                                                      options={sites} onChange={updateTask} isMulti />}
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeTask} disabled={task.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeTask} disabled={task.read_only} back={true}/>
        </div>
        {task.id && <DeleteButton onClick={openDeleteModal} disabled={task.read_only} />}
      </div>

      <DeleteTaskModal task={task} info={info} show={showDeleteModal}
                       onClose={closeDeleteModal} onDelete={deleteTask} />
    </div>
  )
}

EditTask.propTypes = {
  config: PropTypes.object.isRequired,
  task: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default EditTask
