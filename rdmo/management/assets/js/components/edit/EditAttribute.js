import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'

import { fetchElement, storeElement, deleteElement, updateElement } from '../../actions/elementActions'

import Checkbox from './common/Checkbox'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'
import { ReadOnlyIcon } from '../common/Icons'

import AttributeInfo from '../info/AttributeInfo'
import DeleteAttributeModal from '../modals/DeleteAttributeModal'

import useDeleteModal from '../../hooks/useDeleteModal'

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
    <div className="panel panel-default panel-edit">
      <div className="panel-heading">
        <div className="pull-right">
          <ReadOnlyIcon title={gettext('This attribute is read only')} show={attribute.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeAttribute} disabled={attribute.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeAttribute} disabled={attribute.read_only} back={true}/>
        </div>
        {
          attribute.id ? <>
            <strong>{gettext('Attribute')}{': '}</strong>
            <code className="code-domain">{attribute.uri}</code>
          </> : <strong>{gettext('Create attribute')}</strong>
        }
      </div>

      {
        parent && parent.attribute && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This attribute will be added to the attribute <code class="code-domain">%s</code>.'), [parent.attribute.uri])
          }} />
        </div>
      }

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
            __html:interpolate(gettext('This attribute will be added to the question set <code class="code-questions">%s</code>.'), [parent.questionset.uri])
          }} />
        </div>
      }
      {
        parent && parent.question && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This attribute will be added to the question <code class="code-questions">%s</code>.'), [parent.question.uri])
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

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeAttribute} disabled={attribute.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeAttribute} disabled={attribute.read_only} back={true}/>
        </div>
        {attribute.id && <DeleteButton onClick={openDeleteModal} disabled={attribute.read_only} />}
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
