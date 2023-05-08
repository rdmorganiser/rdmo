import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';
import get from 'lodash/get'

import CodeMirror from './common/CodeMirror'
import Checkbox from './common/Checkbox'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'

import ViewInfo from '../info/ViewInfo'
import DeleteViewModal from '../modals/DeleteViewModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditView = ({ config, view, elements, elementActions }) => {

  const { sites, groups } = config
  const { elementAction, catalogs } = elements

  const updateView = (key, value) => elementActions.updateElement(view, {[key]: value})
  const storeView = (back) => elementActions.storeElement('views', view, back)
  const deleteView = () => elementActions.deleteElement('views', view)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <ViewInfo view={view} elements={elements} />

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <SaveButton element={view} elementAction={elementAction} onClick={storeView} />
          <SaveButton element={view} elementAction={elementAction} onClick={storeView} back={true}/>
        </div>
        {
          view.id ? <>
            <strong>{gettext('View')}{': '}</strong>
            <code className="code-views">{view.uri}</code>
          </> : <strong>{gettext('Create view')}</strong>
        }
      </div>

      {
        view.id && <div className="panel-body panel-border">
          { info }
        </div>
      }

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
        </div>

        <Textarea config={config} element={view} field="comment"
                  rows={4} onChange={updateView} />

        <div className="row">
          <div className="col-sm-6">
            <Checkbox config={config} element={view} field="locked"
                      onChange={updateView} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={view} field="available"
                      onChange={updateView} />
          </div>
        </div>

        <Tabs id="#view-tabs" defaultActiveKey={0} animation={false}>
          {
            config.settings && config.settings.languages.map(([lang_code, lang], index) => (
              <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                <Text config={config} element={view} field={`title_${lang_code }`}
                      onChange={updateView} />
                <Textarea config={config} element={view} field={`help_${lang_code }`}
                          rows={8} onChange={updateView} />
              </Tab>
            ))
          }
        </Tabs>

        <Select config={config} element={view} field="catalogs"
                options={catalogs} onChange={updateView} isMulti />

        {get(config, 'settings.groups') && <Select config={config} element={view} field="groups"
                                                   options={groups} onChange={updateView} isMulti />}

        {get(config, 'settings.multisite') && <Select config={config} element={view} field="sites"
                                                      options={sites} onChange={updateView} isMulti />}

        <CodeMirror config={config} element={view} field="template"
                    onChange={updateView} />
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton element={view} elementAction={elementAction} onClick={storeView} />
          <SaveButton element={view} elementAction={elementAction} onClick={storeView} back={true}/>
        </div>
        <DeleteButton element={view} onClick={openDeleteModal} />
      </div>

      <DeleteViewModal view={view} info={info} show={showDeleteModal}
                       onClose={closeDeleteModal} onDelete={deleteView} />
    </div>
  )
}

EditView.propTypes = {
  config: PropTypes.object.isRequired,
  view: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default EditView
