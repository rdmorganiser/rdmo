import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'

import { deleteElement, fetchElement, storeElement, updateElement } from '../../actions/elementActions'
import useDeleteModal from '../../hooks/useDeleteModal'

import { BackButton, DeleteButton, SaveButton } from '../common/Buttons'
import { ReadOnlyIcon } from '../common/Icons'
import AttributeInfo from '../info/AttributeInfo'
import DeleteAttributeModal from '../modals/DeleteAttributeModal'

import Checkbox from './common/Checkbox'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

const EditAttribute = ({ attribute }) => {
  const dispatch = useDispatch()

  const { sites, settings } = useSelector((state) => state.config)
  const { elementAction, parent, attributes } = useSelector((state) => state.elements)

  const editAttribute = (attribute) => dispatch(fetchElement('attributes', attribute))
  const updateAttribute = (key, value) => dispatch(updateElement(attribute, {[key]: value}))
  const storeAttribute = (back) => dispatch(storeElement('attributes', attribute, elementAction, back))
  const deleteAttribute = () => dispatch(deleteElement('attributes', attribute))

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <AttributeInfo attribute={attribute} />

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex flex-wrap align-items-center gap-2">
          <strong className="flex-grow-1">
            {attribute.id ? gettext('Edit attribute') : gettext('Create attribute')}
          </strong>
          <ReadOnlyIcon title={gettext('This attribute is read only')} show={attribute.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeAttribute} disabled={attribute.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeAttribute} disabled={attribute.read_only} back={true}/>
        </div>
      </div>

      {
        parent && parent.attribute && (
          <div className="card-body border-bottom">
            <Html html={
              interpolate(gettext(
                'This attribute will be added to the attribute <code class="code-domain">%s</code>.'),
              [parent.attribute.uri])
            } />
          </div>
        )
      }

      {
        parent && parent.page && (
          <div className="card-body border-bottom">
            <Html html={
              interpolate(gettext(
                'This attribute will be added to the page <code class="code-questions">%s</code>.'),
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
                'This attribute will be added to the question set <code class="code-questions">%s</code>.'),
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
                'This attribute will be added to the question <code class="code-questions">%s</code>.'),
              [parent.question.uri])
            } />
          </div>
        )
      }
      {
        parent && parent.condition && (
          <div className="card-body border-bottom">
            <Html html={
              interpolate(gettext(
                'This attribute will be added to the condition <code class="code-conditions">%s</code>.'),
              [parent.condition.uri])
            } />
          </div>
        )
      }

      {
        attribute.id && (
          <div className="card-body border-bottom">
            {info}
          </div>
        )
      }

      <div className="card-body pb-0">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix element={attribute} field="uri_prefix" onChange={updateAttribute} />
          </div>
          <div className="col-sm-6">
            <Text element={attribute} field="key" onChange={updateAttribute} />
          </div>
        </div>

        <Textarea element={attribute} field="comment" rows={4} onChange={updateAttribute} />

        <Checkbox element={attribute} field="locked" onChange={updateAttribute} />

        <Select element={attribute} field="parent" options={attributes}
          onChange={updateAttribute} onEdit={editAttribute} />

        {
          settings.multisite && (
            <Select element={attribute} field="editors" options={sites} onChange={updateAttribute} isMulti />
          )
        }
      </div>

      <div className="card-footer">
        <div className="d-flex align-items-center gap-2">
          {attribute.id && <DeleteButton onClick={openDeleteModal} disabled={attribute.read_only} />}
          <BackButton className="ms-auto" />
          <SaveButton elementAction={elementAction} onClick={storeAttribute} disabled={attribute.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeAttribute} disabled={attribute.read_only} back={true}/>
        </div>
      </div>

      <DeleteAttributeModal attribute={attribute} info={info} show={showDeleteModal}
        onClose={closeDeleteModal} onDelete={deleteAttribute} />
    </div>
  )
}

EditAttribute.propTypes = {
  attribute: PropTypes.object.isRequired
}

export default EditAttribute
