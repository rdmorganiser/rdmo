import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import { createElement, deleteElement, fetchElement, storeElement, updateElement } from '../../actions/elementActions'
import useDeleteModal from '../../hooks/useDeleteModal'

import { BackButton, DeleteButton, SaveButton } from '../common/Buttons'
import { ReadOnlyIcon } from '../common/Icons'
import TaskInfo from '../info/TaskInfo'
import DeleteTaskModal from '../modals/DeleteTaskModal'

import Checkbox from './common/Checkbox'
import LanguageTabs from './common/LanguageTabs'
import MultiSelect from './common/MultiSelect'
import Number from './common/Number'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

const EditTask = ({ task }) => {
  const dispatch = useDispatch()

  const { sites, groups, settings, taskTypes, taskAreas } = useSelector((state) => state.config)
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
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex flex-wrap align-items-center gap-2">
          <strong className="flex-grow-1">
            {task.id ? gettext('Edit task') : gettext('Create task')}
          </strong>
          <ReadOnlyIcon title={gettext('This task is read only')} show={task.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeTask} disabled={task.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeTask} disabled={task.read_only} back={true}/>
        </div>
      </div>

      {
        task.id && (
          <div className="card-body border-bottom">
            {info}
          </div>
        )
      }

      <div className="card-body pb-0">
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

        <div className="row">
          <div className="col-sm-6">
            <Select element={task} field="task_type" options={taskTypes} onChange={updateTask} />
          </div>
          <div className="col-sm-6">
            <Select element={task} field="task_area" options={taskAreas} onChange={updateTask} />
          </div>
        </div>

        <LanguageTabs render={
          (langCode) => (
            <>
              <Text element={task} field={`title_${langCode}`} onChange={updateTask} />
              <Textarea element={task} field={`text_${langCode}`} rows={8} onChange={updateTask} />
            </>
          )
        } />

        <MultiSelect
          element={task} field="conditions" options={conditions}
          addText={gettext('Add existing condition')} createText={gettext('Create new condition')}
          onChange={updateTask} onCreate={createCondition} onEdit={editCondition} />

        <Select
          element={task} field="start_attribute" options={attributes}
          onChange={updateTask} onEdit={editAttribute} />

        <Select
          element={task} field="end_attribute" options={attributes}
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

      <div className="card-footer">
        <div className="d-flex align-items-center gap-2">
          {task.id && <DeleteButton onClick={openDeleteModal} disabled={task.read_only} />}
          <BackButton className="ms-auto" />
          <SaveButton elementAction={elementAction} onClick={storeTask} disabled={task.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeTask} disabled={task.read_only} back={true}/>
        </div>
      </div>

      <DeleteTaskModal
        task={task} info={info} show={showDeleteModal}
        onClose={closeDeleteModal} onDelete={deleteTask} />
    </div>
  )
}

EditTask.propTypes = {
  task: PropTypes.object.isRequired
}

export default EditTask
