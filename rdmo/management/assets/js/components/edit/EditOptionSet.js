import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Number from '../forms/Number'
import OrderedMultiSelect from '../forms/OrderedMultiSelect'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/ElementButtons'
import { DeleteElementModal } from '../common/ElementModals'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditOptionSet = ({ config, optionset, options, providers, elementActions }) => {

  const updateOptionSet = (key, value) => elementActions.updateElement(optionset, key, value)
  const storeOptionSet = () => elementActions.storeElement('optionsets', optionset)
  const deleteOptionSet = () => elementActions.deleteElement('optionsets', optionset)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <SaveButton onClick={storeOptionSet} />
        </div>
        {
          optionset.id ? <div>
            <strong>{gettext('Option set')}{': '}</strong>
            <code className="code-options">{optionset.uri}</code>
          </div> : <strong>{gettext('Create option set')}</strong>
        }
      </div>

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={optionset} field="uri_prefix"
                       onChange={updateOptionSet} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={optionset} field="uri_path"
                  onChange={updateOptionSet} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={optionset} field="comment"
                      rows={4} onChange={updateOptionSet} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={optionset} field="locked"
                      onChange={updateOptionSet} />
          </div>
          <div className="col-sm-6">
            <Number config={config} element={optionset} field="order"
                    onChange={updateOptionSet} />
          </div>
          <div className="col-sm-12">
            <OrderedMultiSelect config={config} element={optionset} field="options"
                                options={options} verboseName="option"
                                onChange={updateOptionSet} />
          </div>
          <div className="col-sm-12">
            <Select config={config} element={optionset} field="provider_key"
                    options={providers} onChange={updateOptionSet} />
          </div>
        </div>
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton onClick={storeOptionSet} />
        </div>
        <DeleteButton onClick={openDeleteModal} />
      </div>

      <DeleteElementModal title={gettext('Delete catalog')} show={showDeleteModal}
                          onClose={closeDeleteModal} onDelete={deleteOptionSet}>
        <p>
          {gettext('You are about to permanently delete the option set:')}
        </p>
        <p>
          <code className="code-options">{optionset.uri}</code>
        </p>
        <p className="text-danger">
          {gettext('This action cannot be undone!')}
        </p>
      </DeleteElementModal>
    </div>
  )
}

EditOptionSet.propTypes = {
  config: PropTypes.object.isRequired,
  optionset: PropTypes.object.isRequired,
  options: PropTypes.array,
  providers: PropTypes.array,
  elementActions: PropTypes.object.isRequired
}

export default EditOptionSet
