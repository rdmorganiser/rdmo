import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'

import AttributeInfo from '../info/AttributeInfo'
import DeleteAttributeModal from '../modals/DeleteAttributeModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditAttribute = ({ config, attribute, elements, elementActions }) => {

  const { parent, attributes, conditions, pages, questionsets, questions, tasks } = elements

  const updateAttribute = (key, value) => elementActions.updateElement(attribute, {[key]: value})
  const storeAttribute = (back) => elementActions.storeElement('attributes', attribute, back)
  const deleteAttribute = () => elementActions.deleteElement('attributes', attribute)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <AttributeInfo attribute={attribute} elements={elements} />

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <SaveButton element={attribute} onClick={storeAttribute} />
          <SaveButton element={attribute} onClick={storeAttribute} back={true}/>
        </div>
        {
          attribute.id ? <>
            <strong>{gettext('Attribute')}{': '}</strong>
            <code className="code-domain">{attribute.uri}</code>
          </> : <strong>{gettext('Create attribute')}</strong>
        }
      </div>

      {
        parent && parent.page && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This attribute will be added to the page <code class="code-questions">%s</code>.'), [parent.page.uri])
          }} />
        </div>
      }
      {
        parent && parent.questionset && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This attribute will be added to the page <code class="code-questions">%s</code>.'), [parent.questionset.uri])
          }} />
        </div>
      }
      {
        parent && parent.question && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This attribute will be added to the page <code class="code-questions">%s</code>.'), [parent.question.uri])
          }} />
        </div>
      }
      {
        parent && parent.condition && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This attribute will be added to the condition <code class="code-conditions">%s</code>.'), [parent.condition.uri])
          }} />
        </div>
      }

      {
        attribute.id && <div className="panel-body panel-border">
          { info }
        </div>
      }

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
        </div>

        <Textarea config={config} element={attribute} field="comment"
                  rows={4} onChange={updateAttribute} />

        <Checkbox config={config} element={attribute} field="locked"
                  onChange={updateAttribute} />

        <Select config={config} element={attribute} field="parent"
                options={attributes} onChange={updateAttribute} />
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton element={attribute} onClick={storeAttribute} />
          <SaveButton element={attribute} onClick={storeAttribute} back={true}/>
        </div>
        <DeleteButton element={attribute} onClick={openDeleteModal} />
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
