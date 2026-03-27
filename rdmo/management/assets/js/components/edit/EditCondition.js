import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'

import { createElement, deleteElement, fetchElement, storeElement, updateElement } from '../../actions/elementActions'
import useDeleteModal from '../../hooks/useDeleteModal'

import { BackButton, DeleteButton, SaveButton } from '../common/Buttons'
import { ReadOnlyIcon } from '../common/Icons'
import ConditionInfo from '../info/ConditionInfo'
import DeleteConditionModal from '../modals/DeleteConditionModal'

import Checkbox from './common/Checkbox'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

const EditCondition = ({ condition }) => {
  const dispatch = useDispatch()

  const { sites, relations, settings } = useSelector((state) => state.config)
  const { elementAction, parent, attributes, options } = useSelector((state) => state.elements)

  const updateCondition = (key, value) => dispatch(updateElement(condition, {[key]: value}))
  const storeCondition = (back) => dispatch(storeElement('conditions', condition, elementAction, back))
  const deleteCondition = () => dispatch(deleteElement('conditions', condition))

  const editAttribute = (attribute) => dispatch(fetchElement('attributes', attribute))
  const createAttribute = () => dispatch(createElement('attributes', { condition }))

  const editOption = (option) => dispatch(fetchElement('options', option))

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <ConditionInfo condition={condition} />

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex flex-wrap align-items-center gap-2">
          <strong className="flex-grow-1">
            {condition.id ? gettext('Edit condition') : gettext('Create condition')}
          </strong>
          <ReadOnlyIcon title={gettext('This condition is read only')} show={condition.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeCondition} disabled={condition.read_only} />
          <SaveButton
            elementAction={elementAction}
            onClick={storeCondition}
            disabled={condition.read_only}
            back={true}
          />
        </div>
      </div>

      {
        parent && parent.optionset && (
          <div className="card-body border-bottom">
            <Html html={
              interpolate(gettext(
                'This condition will be added to the option set <code class="code-options">%s</code>.'),
              [parent.optionset.uri])
            } />
          </div>
        )
      }
      {
        parent && parent.page && (
          <div className="card-body border-bottom">
            <Html html={
              interpolate(gettext(
                'This condition will be added to the page <code class="code-questions">%s</code>.'),
              [parent.page.uri])
            } />
          </div>
        )
      }
      {
        parent && parent.questionset && (
          <div className="card-body border-bottom">
            <Html html={
              interpolate(gettext(
                'This condition will be added to the question set <code class="code-questions">%s</code>.'),
              [parent.questionset.uri])
            } />
          </div>
        )
      }
      {
        parent && parent.question && (
          <div className="card-body border-bottom">
            <Html html={
              interpolate(gettext(
                'This condition will be added to the question <code class="code-questions">%s</code>.'),
              [parent.question.uri])
            } />
          </div>
        )
      }
      {
        parent && parent.task && (
          <div className="card-body border-bottom">
            <Html html={
              interpolate(gettext(
                'This condition will be added to the task <code class="code-tasks">%s</code>.'),
              [parent.task.uri])
            } />
          </div>
        )
      }

      {
        condition.id && (
          <div className="card-body border-bottom">
            {info}
          </div>
        )
      }

      <div className="card-body pb-0">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix element={condition} field="uri_prefix" onChange={updateCondition} />
          </div>
          <div className="col-sm-6">
            <Text element={condition} field="uri_path" onChange={updateCondition} />
          </div>
        </div>

        <Textarea element={condition} field="comment" rows={4} onChange={updateCondition} />

        <Checkbox element={condition} field="locked" onChange={updateCondition} />

        <Select element={condition} field="source" createText={gettext('Create new attribute')}
          options={attributes} onChange={updateCondition} onCreate={createAttribute} onEdit={editAttribute} />

        <Select element={condition} field="relation" options={relations} onChange={updateCondition} />

        <Text element={condition} field="target_text" onChange={updateCondition} />

        <Select
          element={condition}
          field="target_option"
          options={options}
          onChange={updateCondition}
          onEdit={editOption}
        />

        {
          settings.multisite && (
            <Select element={condition} field="editors" options={sites} onChange={updateCondition} isMulti />
          )
        }
      </div>

      <div className="card-footer">
        <div className="d-flex align-items-center gap-2">
          {condition.id && <DeleteButton onClick={openDeleteModal} disabled={condition.read_only} />}
          <BackButton className="ms-auto" />
          <SaveButton elementAction={elementAction} onClick={storeCondition} disabled={condition.read_only} />
          <SaveButton
            elementAction={elementAction}
            onClick={storeCondition}
            disabled={condition.read_only}
            back={true}
          />
        </div>
      </div>

      <DeleteConditionModal condition={condition} info={info} show={showDeleteModal}
        onClose={closeDeleteModal} onDelete={deleteCondition} />
    </div>
  )
}

EditCondition.propTypes = {
  condition: PropTypes.object.isRequired
}

export default EditCondition
