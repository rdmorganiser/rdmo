import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import { BackButton, SaveButton, CreateButton, DeleteButton } from '../common/ElementButtons'

import AttributeInfo from '../info/AttributeInfo'
import DeleteAttributeModal from '../modals/DeleteAttributeModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditAttribute = ({ config, attribute, elements, elementActions }) => {

  const { attributes, conditions, pages, questionsets, questions, tasks } = elements

  const updateAttribute = (key, value) => elementActions.updateElement(attribute, key, value)
  const storeAttribute = () => elementActions.storeElement('attributes', attribute)
  const deleteAttribute = () => elementActions.deleteElement('attributes', attribute)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <AttributeInfo attribute={attribute} elements={elements} />

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          {
            attribute.id ? <SaveButton onClick={storeAttribute} />
                         : <CreateButton onClick={storeAttribute} />
          }
        </div>
        {
          attribute.id ? <div>
            <strong>{gettext('Attribute')}{': '}</strong>
            <code className="code-domain">{attribute.uri}</code>
          </div> : <strong>{gettext('Create attribute')}</strong>
        }
      </div>

      <div className="panel-body panel-border">
        { info }
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
          {
            attribute.id ? <SaveButton onClick={storeAttribute} />
                         : <CreateButton onClick={storeAttribute} />
          }
        </div>
        {attribute.id && <DeleteButton onClick={openDeleteModal} />}
      </div>

      <DeleteAttributeModal attribute={attribute} info={info} show={showDeleteModal}
                            onClose={closeDeleteModal} onDelete={deleteAttribute} />
    </div>
  )
}

EditAttribute.propTypes = {
  config: PropTypes.object.isRequired,
  attribute: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default EditAttribute
