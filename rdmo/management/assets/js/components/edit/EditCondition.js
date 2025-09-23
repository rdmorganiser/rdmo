import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'

import { fetchElement, storeElement, createElement, deleteElement, updateElement } from '../../actions/elementActions'

import Checkbox from './common/Checkbox'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'
import { ReadOnlyIcon } from '../common/Icons'

import ConditionInfo from '../info/ConditionInfo'
import DeleteConditionModal from '../modals/DeleteConditionModal'

import useDeleteModal from '../../hooks/useDeleteModal'

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
    <div className="panel panel-default panel-edit">
      <div className="panel-heading">
        <div className="pull-right">
          <ReadOnlyIcon title={gettext('This condition is read only')} show={condition.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeCondition} disabled={condition.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeCondition} disabled={condition.read_only} back={true}/>
        </div>
        {
          condition.id ? <>
            <strong>{gettext('Condition')}{': '}</strong>
            <code className="code-conditions">{condition.uri}</code>
          </> : <strong>{gettext('Create condition')}</strong>
        }
      </div>

      {
        parent && parent.optionset && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This condition will be added to the option set <code class="code-options">%s</code>.'), [parent.optionset.uri])
          }} />
        </div>
      }
      {
        parent && parent.page && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This condition will be added to the page <code class="code-questions">%s</code>.'), [parent.page.uri])
          }} />
        </div>
      }
      {
        parent && parent.questionset && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This condition will be added to the question set <code class="code-questions">%s</code>.'), [parent.questionset.uri])
          }} />
        </div>
      }
      {
        parent && parent.question && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This condition will be added to the question <code class="code-questions">%s</code>.'), [parent.question.uri])
          }} />
        </div>
      }
      {
        parent && parent.task && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This condition will be added to the task <code class="code-tasks">%s</code>.'), [parent.task.uri])
          }} />
        </div>
      }

      {
        condition.id && <div className="panel-body panel-border">
          { info }
        </div>
      }

      <div className="panel-body">
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

        <Select element={condition} field="target_option" options={options} onChange={updateCondition} onEdit={editOption} />

        {
          settings.multisite && (
            <Select element={condition} field="editors" options={sites} onChange={updateCondition} isMulti />
          )
        }
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeCondition} disabled={condition.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeCondition} disabled={condition.read_only} back={true}/>
        </div>
        {condition.id && <DeleteButton onClick={openDeleteModal} disabled={condition.read_only} />}
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
