import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'

import ConditionInfo from '../info/ConditionInfo'
import DeleteConditionModal from '../modals/DeleteConditionModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditCondition = ({ config, condition, elements, elementActions }) => {

  const { relations, attributes, optionsets, options, pages, questionsets, questions, tasks } = elements

  const updateCondition = (key, value) => elementActions.updateElement(condition, {[key]: value})
  const storeCondition = (back) => elementActions.storeElement('conditions', condition, back)
  const deleteCondition = () => elementActions.deleteElement('conditions', condition)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <ConditionInfo condition={condition} elements={elements} />

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <SaveButton element={condition} onClick={storeCondition} />
          <SaveButton element={condition} onClick={storeCondition} back={true}/>
        </div>
        {
          condition.id ? <>
            <strong>{gettext('Condition')}{': '}</strong>
            <code className="code-conditions">{condition.uri}</code>
          </> : <strong>{gettext('Create condition')}</strong>
        }
      </div>

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

        <div className="row">
          <div className="col-sm-6">
            <Select config={config} element={condition} field="source"
                    options={attributes} onChange={updateCondition} />
          </div>
          <div className="col-sm-6">
            <Select config={config} element={condition} field="relation"
                    options={relations} onChange={updateCondition} />
          </div>
        </div>

        <div className="row">
          <div className="col-sm-6">
            <Text config={config} element={condition} field="target_text"
                  onChange={updateCondition} />
          </div>
          <div className="col-sm-6">
            <Select config={config} element={condition} field="target_option"
                    options={options} onChange={updateCondition} />
          </div>
        </div>
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton element={condition} onClick={storeCondition} />
          <SaveButton element={condition} onClick={storeCondition} back={true}/>
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
