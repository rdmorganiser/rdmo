import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/ElementButtons'
import { DeleteElementModal } from '../common/ElementModals'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditOption = ({ config, option, elementActions }) => {

  const updateOption = (key, value) => elementActions.updateElement(option, key, value)
  const storeOption = () => elementActions.storeElement('options', option)
  const deleteOption = () => elementActions.deleteElement('options', option)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <SaveButton onClick={storeOption} />
        </div>
        {
          option.id ? <div>
            <strong>{gettext('Option')}{': '}</strong>
            <code className="code-options">{option.uri}</code>
          </div> : <strong>{gettext('Create option')}</strong>
        }
      </div>

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={option} field="uri_prefix"
                       onChange={updateOption} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={option} field="uri_path"
                  onChange={updateOption} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={option} field="comment"
                      rows={4} onChange={updateOption} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={option} field="locked"
                      onChange={updateOption} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={option} field="additional_input"
                      onChange={updateOption} />
          </div>
          <div className="col-sm-12">
            <Tabs id="#option-tabs" defaultActiveKey={0} animation={false}>
              {
                config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                  return (
                    <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                      <div className="row">
                        <div className="col-sm-12">
                          <Text config={config} element={option} field={`text_${lang_code }`}
                                onChange={updateOption} />
                        </div>
                      </div>
                    </Tab>
                  )
                })
              }
            </Tabs>
          </div>
        </div>
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton onClick={storeOption} />
        </div>
        <DeleteButton onClick={openDeleteModal} />
      </div>

      <DeleteElementModal title={gettext('Delete catalog')} show={showDeleteModal}
                          onClose={closeDeleteModal} onDelete={deleteOption}>
        <p>
          {gettext('You are about to permanently delete the option:')}
        </p>
        <p>
          <code className="code-options">{option.uri}</code>
        </p>
        <p className="text-danger">
          {gettext('This action cannot be undone!')}
        </p>
      </DeleteElementModal>
    </div>
  )
}

EditOption.propTypes = {
  config: PropTypes.object.isRequired,
  option: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default EditOption
