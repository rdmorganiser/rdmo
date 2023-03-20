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

const EditAttribute = ({ config, attribute, attributes, elementActions }) => {

  const updateAttribute = (key, value) => elementActions.updateElement(attribute, key, value)
  const storeAttribute = () => elementActions.storeElement('attributes', attribute)
  const deleteAttribute = () => elementActions.deleteElement('attributes', attribute)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <SaveButton onClick={storeAttribute} />
          <DeleteButton onClick={openDeleteModal} />
        </div>
        {
          attribute.id ? <div>
            <strong>{gettext('Attribute')}{': '}</strong>
            <code className="code-domain">{attribute.uri}</code>
          </div> : <strong>{gettext('Create attribute')}</strong>
        }
      </div>

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={attribute} field="uri_prefix"
                       onChange={updateAttribute} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={attribute} field="key"
                  onChange={updateAttribute} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={attribute} field="comment"
                      rows={4} onChange={updateAttribute} />
          </div>
          <div className="col-sm-12">
            <Checkbox config={config} element={attribute} field="locked"
                      onChange={updateAttribute} />
          </div>
          <div className="col-sm-12">
            <Select config={config} element={attribute} field="parent"
                    options={attributes} onChange={updateAttribute} />
          </div>
        </div>
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton onClick={storeAttribute} />
        </div>
        <DeleteButton onClick={openDeleteModal} />
      </div>

      <DeleteElementModal title={gettext('Delete catalog')} show={showDeleteModal}
                          onClose={closeDeleteModal} onDelete={deleteAttribute}>
        <p>
          {gettext('You are about to permanently delete the attribute:')}
        </p>
        <p>
          <code className="code-domain">{attribute.uri}</code>
        </p>
        <p className="text-danger">
          {gettext('This action cannot be undone!')}
        </p>
      </DeleteElementModal>
    </div>
  )
}

EditAttribute.propTypes = {
  config: PropTypes.object.isRequired,
  attribute: PropTypes.object.isRequired,
  attributes: PropTypes.array,
  elementActions: PropTypes.object.isRequired
}

export default EditAttribute
