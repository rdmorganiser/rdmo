import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from './common/Checkbox'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'

import ConditionInfo from '../info/ConditionInfo'
import DeleteConditionModal from '../modals/DeleteConditionModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditCondition = ({ config, condition, elements, elementActions }) => {

  const { relations } = config
  const { elementAction, parent, attributes, optionsets, options,
          pages, questionsets, questions, tasks } = elements

  const updateCondition = (key, value) => elementActions.updateElement(condition, {[key]: value})
  const storeCondition = (back) => elementActions.storeElement('conditions', condition, back)
  const deleteCondition = () => elementActions.deleteElement('conditions', condition)

  const editAttribute = (attribute) => elementActions.fetchElement('attributes', attribute)
  const createAttribute = () => elementActions.createElement('attributes', { condition })

  const editOption = (option) => elementActions.fetchElement('options', option)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <ConditionInfo condition={condition} elements={elements} elementActions={elementActions} />

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <SaveButton element={condition} elementAction={elementAction} onClick={storeCondition} />
          <SaveButton element={condition} elementAction={elementAction} onClick={storeCondition} back={true}/>
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
            <UriPrefix config={config} element={condition} field="uri_prefix"
                       onChange={updateCondition} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={condition} field="key"
                  onChange={updateCondition} />
          </div>
        </div>

        <Textarea config={config} element={condition} field="comment"
                  rows={4} onChange={updateCondition} />

        <Checkbox config={config} element={condition} field="locked"
                  onChange={updateCondition} />

        <Select config={config} element={condition} field="source" verboseName={gettext('attribute')}
                options={attributes} onChange={updateCondition} onCreate={createAttribute} onEdit={editAttribute} />

        <Select config={config} element={condition} field="relation"
                options={relations} onChange={updateCondition} />

        <Text config={config} element={condition} field="target_text" onChange={updateCondition} />

        <Select config={config} element={condition} field="target_option"
                options={options} onChange={updateCondition} onEdit={editOption} />
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton element={condition} elementAction={elementAction} onClick={storeCondition} />
          <SaveButton element={condition} elementAction={elementAction} onClick={storeCondition} back={true}/>
        </div>
        <DeleteButton element={condition} onClick={openDeleteModal} />
      </div>

      <DeleteConditionModal condition={condition} info={info} show={showDeleteModal}
                            onClose={closeDeleteModal} onDelete={deleteCondition} />
    </div>
  )
}

EditCondition.propTypes = {
  config: PropTypes.object.isRequired,
  condition: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default EditCondition
