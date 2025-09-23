import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap'

import { fetchElement, storeElement, createElement, deleteElement, updateElement } from '../../actions/elementActions'

import Checkbox from './common/Checkbox'
import Number from './common/Number'
import OrderedMultiSelect from './common/OrderedMultiSelect'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'
import { ReadOnlyIcon } from '../common/Icons'

import CatalogInfo from '../info/CatalogInfo'
import DeleteCatalogModal from '../modals/DeleteCatalogModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditCatalog = ({ catalog }) => {
  const dispatch = useDispatch()

  const { groups, sites, settings } = useSelector((state) => state.config)
  const { elementAction, sections } = useSelector((state) => state.elements)

  const updateCatalog = (key, value) => dispatch(updateElement(catalog, {[key]: value}))
  const storeCatalog = (back) => dispatch(storeElement('catalogs', catalog, elementAction, back))
  const deleteCatalog = () => dispatch(deleteElement('catalogs', catalog))

  const editSection = (value) => dispatch(fetchElement('sections', value.section))
  const createSection = () => dispatch(createElement('sections', { catalog } ))

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <CatalogInfo catalog={catalog} />

  // for reasons unknown, the strings are not picked up by makemessages from the props
  const addSectionText = gettext('Add existing section')
  const createSectionText = gettext('Create new section')

  return (
    <div className="panel panel-default panel-edit">
      <div className="panel-heading">
        <div className="pull-right">
          <ReadOnlyIcon title={gettext('This catalog is read only')} show={catalog.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeCatalog} disabled={catalog.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeCatalog} disabled={catalog.read_only} back={true}/>
        </div>
        {
          catalog.id ? <>
            <strong>{gettext('Catalog')}{': '}</strong>
            <code className="code-questions">{catalog.uri}</code>
          </> : <strong>{gettext('Create catalog')}</strong>
        }
      </div>

      {
        catalog.id && <div className="panel-body panel-border">
          { info }
        </div>
      }

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix element={catalog} field="uri_prefix" onChange={updateCatalog} />
          </div>
          <div className="col-sm-6">
            <Text element={catalog} field="uri_path" onChange={updateCatalog} />
          </div>
        </div>

        <Textarea element={catalog} field="comment" rows={4} onChange={updateCatalog} />

        <div className="row">
          <div className="col-sm-4">
            <Checkbox element={catalog} field="locked" onChange={updateCatalog} />
          </div>
          <div className="col-sm-4">
            <Checkbox element={catalog} field="available" onChange={updateCatalog} />
          </div>
          <div className="col-sm-4">
            <Number element={catalog} field="order" onChange={updateCatalog} />
          </div>
        </div>

        <Tabs id="#catalog-tabs" defaultActiveKey={0} animation={false}>
          {
            settings.languages.map(([lang_code, lang], index) => (
              <Tab key={index} eventKey={index} title={lang}>
                <Text element={catalog} field={`title_${lang_code }`} onChange={updateCatalog} />
                <Textarea element={catalog} field={`help_${lang_code }`}
                          rows={4} onChange={updateCatalog} />
              </Tab>
            ))
          }
        </Tabs>

        <OrderedMultiSelect element={catalog} field="sections" options={sections}
                            addText={addSectionText} createText={createSectionText}
                            onChange={updateCatalog} onCreate={createSection} onEdit={editSection} />

        {
          settings.groups && (
            <Select element={catalog} field="groups" options={groups} onChange={updateCatalog} isMulti />
          )
        }
        {
          settings.multisite && (
            <>
              <Select element={catalog} field="sites" options={sites} onChange={updateCatalog} isMulti />
              <Select element={catalog} field="editors" options={sites} onChange={updateCatalog} isMulti />
            </>
          )
        }
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeCatalog} disabled={catalog.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeCatalog} disabled={catalog.read_only} back={true} />
        </div>
        {catalog.id && <DeleteButton onClick={openDeleteModal} disabled={catalog.read_only} />}
      </div>

      <DeleteCatalogModal catalog={catalog} info={info} show={showDeleteModal}
                          onClose={closeDeleteModal} onDelete={deleteCatalog} />
    </div>
  )
}

EditCatalog.propTypes = {
  catalog: PropTypes.object.isRequired
}

export default EditCatalog
