import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Number from '../forms/Number'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'

import TaskInfo from '../info/TaskInfo'
import DeleteTaskModal from '../modals/DeleteTaskModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditTask = ({ config, task, elements, elementActions}) => {

  const { attributes, catalogs, sites, groups } = elements

  const updateTask = (key, value) => elementActions.updateElement(task, {[key]: value})
  const storeTask = (back) => elementActions.storeElement('tasks', task, back)
  const deleteTask = () => elementActions.deleteElement('tasks', task)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <TaskInfo task={task} elements={elements} />

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <SaveButton element={task} onClick={storeTask} />
          <SaveButton element={task} onClick={storeTask} back={true}/>
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
            <Text config={config} element={task} field="key"
                  onChange={updateTask} />
          </div>
        </div>

        <Textarea config={config} element={task} field="comment"
                  rows={4} onChange={updateTask} />

        <div className="row">
          <div className="col-sm-6">
            <Checkbox config={config} element={task} field="locked"
                      onChange={updateTask} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={task} field="available"
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

        <Select config={config} element={task} field="start_attribute"
                options={attributes} onChange={updateTask} />

        <Select config={config} element={task} field="end_attribute"
                options={attributes} onChange={updateTask} />

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
                options={catalogs} onChange={updateTask} />

        <div className="row">
          <div className="col-sm-6">
            <Select config={config} element={task} field="groups"
                    options={groups} onChange={updateTask} />
          </div>
          <div className="col-sm-6">
            <Select config={config} element={task} field="sites"
                    options={sites} onChange={updateTask} />
          </div>
        </div>
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton element={task} onClick={storeTask} />
          <SaveButton element={task} onClick={storeTask} back={true}/>
        </div>
        <DeleteButton element={task} onClick={openDeleteModal} />
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
