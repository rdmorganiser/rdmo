import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap'

import { storeElement, deleteElement, updateElement } from '../../actions/elementActions'

import CodeMirror from './common/CodeMirror'
import Checkbox from './common/Checkbox'
import Number from './common/Number'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'
import { ReadOnlyIcon } from '../common/Icons'

import ViewInfo from '../info/ViewInfo'
import DeleteViewModal from '../modals/DeleteViewModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditView = ({ view }) => {
  const dispatch = useDispatch()

  const { sites, groups, settings } = useSelector((state) => state.config)
  const { elementAction, catalogs } = useSelector((state) => state.elements)

  const updateView = (key, value) => dispatch(updateElement(view, {[key]: value}))
  const storeView = (back) => dispatch(storeElement('views', view, elementAction, back))
  const deleteView = () => dispatch(deleteElement('views', view))

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <ViewInfo view={view} />

  return (
    <div className="panel panel-default panel-edit">
      <div className="panel-heading">
        <div className="pull-right">
          <ReadOnlyIcon title={gettext('This view is read only')} show={view.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeView} disabled={view.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeView} disabled={view.read_only} back={true}/>
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
            <UriPrefix element={view} field="uri_prefix" onChange={updateView} />
          </div>
          <div className="col-sm-6">
            <Text element={view} field="uri_path" onChange={updateView} />
          </div>
        </div>

        <Textarea element={view} field="comment" rows={4} onChange={updateView} />

        <div className="row">
          <div className="col-sm-4">
            <Checkbox element={view} field="locked" onChange={updateView} />
          </div>
          <div className="col-sm-4">
            <Checkbox element={view} field="available" onChange={updateView} />
          </div>
          <div className="col-sm-4">
            <Number element={view} field="order" onChange={updateView} />
          </div>
        </div>

        <Tabs id="#view-tabs" defaultActiveKey={0} animation={false}>
          {
            settings.languages.map(([lang_code, lang], index) => (
              <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                <Text element={view} field={`title_${lang_code }`} onChange={updateView} />
                <Textarea element={view} field={`help_${lang_code }`} rows={8} onChange={updateView} />
              </Tab>
            ))
          }
        </Tabs>

        <Select element={view} field="catalogs" options={catalogs} onChange={updateView} isMulti />

        {
          settings.groups && (
            <Select element={view} field="groups" options={groups} onChange={updateView} isMulti />
          )
        }
        {
          settings.multisite && (
            <>
              <Select element={view} field="sites" options={sites} onChange={updateView} isMulti />
              <Select element={view} field="editors" options={sites} onChange={updateView} isMulti />
            </>
          )
        }

        <CodeMirror element={view} field="template" onChange={updateView} />
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeView} disabled={view.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeView} disabled={view.read_only} back={true}/>
        </div>
        {view.id && <DeleteButton onClick={openDeleteModal} disabled={view.read_only} />}
      </div>

      <DeleteViewModal view={view} info={info} show={showDeleteModal}
                       onClose={closeDeleteModal} onDelete={deleteView} />
    </div>
  )
}

EditView.propTypes = {
  view: PropTypes.object.isRequired
}

export default EditView
