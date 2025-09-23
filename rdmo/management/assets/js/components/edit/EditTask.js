import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap'

import { fetchElement, storeElement, createElement, deleteElement, updateElement } from '../../actions/elementActions'

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

const EditTask = ({ task }) => {
  const dispatch = useDispatch()

  const { sites, groups, settings } = useSelector((state) => state.config)
  const { elementAction, attributes, catalogs, conditions } = useSelector((state) => state.elements)

  const updateTask = (key, value) => dispatch(updateElement(task, {[key]: value}))
  const storeTask = (back) => dispatch(storeElement('tasks', task, elementAction, back))
  const deleteTask = () => dispatch(deleteElement('tasks', task))

  const editCondition = (condition) => dispatch(fetchElement('conditions', condition))
  const createCondition = () => dispatch(createElement('conditions', { task }))

  const editAttribute = (attribute) => dispatch(fetchElement('attributes', attribute))

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <TaskInfo task={task} />

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
            <UriPrefix element={task} field="uri_prefix" onChange={updateTask} />
          </div>
          <div className="col-sm-6">
            <Text element={task} field="uri_path" onChange={updateTask} />
          </div>
        </div>

        <Textarea element={task} field="comment" rows={4} onChange={updateTask} />

        <div className="row">
          <div className="col-sm-4">
            <Checkbox element={task} field="locked" onChange={updateTask} />
          </div>
          <div className="col-sm-4">
            <Checkbox element={task} field="available" onChange={updateTask} />
          </div>
          <div className="col-sm-4">
            <Number element={task} field="order" onChange={updateTask} />
          </div>
        </div>

        <Tabs id="#task-tabs" defaultActiveKey={0} animation={false}>
          {
            settings.languages.map(([lang_code, lang], index) => (
              <Tab key={index} eventKey={index} title={lang}>
                <Text element={task} field={`title_${lang_code }`} onChange={updateTask} />
                <Textarea element={task} field={`text_${lang_code }`} rows={8} onChange={updateTask} />
              </Tab>
            ))
          }
        </Tabs>

        <MultiSelect element={task} field="conditions" options={conditions}
                     addText={gettext('Add existing condition')} createText={gettext('Create new condition')}
                     onChange={updateTask} onCreate={createCondition} onEdit={editCondition} />

        <Select element={task} field="start_attribute" options={attributes}
                onChange={updateTask} onEdit={editAttribute} />

        <Select element={task} field="end_attribute" options={attributes}
                onChange={updateTask} onEdit={editAttribute} />

        <div className="row">
          <div className="col-sm-6">
            <Number element={task} field="days_before" onChange={updateTask} />
          </div>
          <div className="col-sm-6">
            <Number element={task} field="days_after" onChange={updateTask} />
          </div>
        </div>

        <Select element={task} field="catalogs" options={catalogs} onChange={updateTask} isMulti />

        {
          settings.groups && (
            <Select element={task} field="groups" options={groups} onChange={updateTask} isMulti />
          )
        }
        {
          settings.multisite && (
            <>
              <Select element={task} field="sites" options={sites} onChange={updateTask} isMulti />
              <Select element={task} field="editors" options={sites} onChange={updateTask} isMulti />
            </>
          )
        }
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
  task: PropTypes.object.isRequired
}

export default EditTask
