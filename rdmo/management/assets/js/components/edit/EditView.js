import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import CodeMirror from '../forms/CodeMirror'
import Checkbox from '../forms/Checkbox'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/ElementButtons'
import { DeleteElementModal } from '../common/ElementModals'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditView = ({ config, view, catalogs, sites, groups, elementActions }) => {

  const updateView = (key, value) => elementActions.updateElement(view, key, value)
  const storeView = () => elementActions.storeElement('views', view)
  const deleteView = () => elementActions.deleteElement('views', view)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <SaveButton onClick={storeView} />
        </div>
        {
          view.id ? <div>
            <strong>{gettext('View')}{': '}</strong>
            <code className="code-views">{view.uri}</code>
          </div> : <strong>{gettext('Create view')}</strong>
        }
      </div>

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={view} field="uri_prefix"
                       onChange={updateView} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={view} field="key"
                  onChange={updateView} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={view} field="comment"
                      rows={4} onChange={updateView} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={view} field="locked"
                      onChange={updateView} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={view} field="available"
                      onChange={updateView} />
          </div>
          <div className="col-sm-12">
            <CodeMirror config={config} element={view} field="template"
                        onChange={updateView} />
          </div>
          <div className="col-sm-12">
            <Tabs id="#view-tabs" defaultActiveKey={0} animation={false}>
              {
                config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                  return (
                    <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                      <Text config={config} element={view} field={`title_${lang_code }`}
                            onChange={updateView} />
                      <Textarea config={config} element={view} field={`help_${lang_code }`}
                                rows={8} onChange={updateView} />
                    </Tab>
                  )
                })
              }
              <Tab className="pt-10" eventKey={config.settings.languages.length + 1} title={gettext('Visibility')}>
                <Select config={config} element={view} field="catalogs"
                        options={catalogs} onChange={updateView} />
                <Select config={config} element={view} field="groups"
                        options={groups} onChange={updateView} />
                <Select config={config} element={view} field="sites"
                        options={sites} onChange={updateView} />
              </Tab>
            </Tabs>
          </div>
        </div>
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton onClick={storeView} />
        </div>
        <DeleteButton onClick={openDeleteModal} />
      </div>

      <DeleteElementModal title={gettext('Delete catalog')} show={showDeleteModal}
                          onClose={closeDeleteModal} onDelete={deleteView}>
        <p>
          {gettext('You are about to permanently delete the view:')}
        </p>
        <p>
          <code className="code-views">{view.uri}</code>
        </p>
        <p className="text-danger">
          {gettext('This action cannot be undone!')}
        </p>
      </DeleteElementModal>
    </div>
  )
}

EditView.propTypes = {
  config: PropTypes.object.isRequired,
  view: PropTypes.object.isRequired,
  catalogs: PropTypes.array,
  groups: PropTypes.array,
  sites: PropTypes.array,
  elementActions: PropTypes.object.isRequired
}

export default EditView
