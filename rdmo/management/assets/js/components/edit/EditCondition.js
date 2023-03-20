import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/ElementButtons'
import { DeleteElementModal } from '../common/ElementModals'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditCondition = ({ config, condition, relations, attributes, options, elementActions }) => {

  const updateCondition = (key, value) => elementActions.updateElement(condition, key, value)
  const storeCondition = () => elementActions.storeElement('conditions', condition)
  const deleteCondition = () => elementActions.deleteElement('conditions', condition)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <SaveButton onClick={storeCondition} />
        </div>
        {
          condition.id ? <div>
            <strong>{gettext('Condition')}{': '}</strong>
            <code className="code-conditions">{condition.uri}</code>
          </div> : <strong>{gettext('Create condition')}</strong>
        }
      </div>

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
          <div className="col-sm-12">
            <Textarea config={config} element={condition} field="comment"
                      rows={4} onChange={updateCondition} />
          </div>
          <div className="col-sm-12">
            <Checkbox config={config} element={condition} field="locked"
                      onChange={updateCondition} />
          </div>
          <div className="col-sm-6">
            <Select config={config} element={condition} field="source"
                    options={attributes} onChange={updateCondition} />
          </div>
          <div className="col-sm-6">
            <Select config={config} element={condition} field="relation"
                    options={relations} onChange={updateCondition} />
          </div>
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
          <SaveButton onClick={storeCondition} />
        </div>
        <DeleteButton onClick={openDeleteModal} />
      </div>

      <DeleteElementModal title={gettext('Delete catalog')} show={showDeleteModal}
                          onClose={closeDeleteModal} onDelete={deleteCondition}>
        <p>
          {gettext('You are about to permanently delete the condition:')}
        </p>
        <p>
          <code className="code-conditions">{condition.uri}</code>
        </p>
        <p className="text-danger">
          {gettext('This action cannot be undone!')}
        </p>
      </DeleteElementModal>
    </div>
  )
}

EditCondition.propTypes = {
  config: PropTypes.object.isRequired,
  condition: PropTypes.object.isRequired,
  relations: PropTypes.array,
  attributes: PropTypes.array,
  options: PropTypes.array,
  elementActions: PropTypes.object.isRequired
}

export default EditCondition
