import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import { createElement, deleteElement, fetchElement, storeElement, updateElement } from '../../actions/elementActions'
import useDeleteModal from '../../hooks/useDeleteModal'

import { BackButton, DeleteButton, SaveButton } from '../common/Buttons'
import { ReadOnlyIcon } from '../common/Icons'
import CatalogInfo from '../info/CatalogInfo'
import DeleteCatalogModal from '../modals/DeleteCatalogModal'

import Checkbox from './common/Checkbox'
import LanguageTabs from './common/LanguageTabs'
import Number from './common/Number'
import OrderedMultiSelect from './common/OrderedMultiSelect'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

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
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex align-items-center gap-2">
          <strong className="flex-grow-1">
            {catalog.id ? gettext('Edit catalog') : gettext('Create catalog')}
          </strong>
          <ReadOnlyIcon title={gettext('This catalog is read only')} show={catalog.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeCatalog} disabled={catalog.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeCatalog} disabled={catalog.read_only} back={true}/>
        </div>
      </div>

      {
        catalog.id && <div className="card-body border-bottom">
          { info }
        </div>
      }

      <div className="card-body pb-0">
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

        <LanguageTabs render={
          (langCode) => (
            <div>
              <Text element={catalog} field={`title_${langCode }`} onChange={updateCatalog} />
              <Textarea element={catalog} field={`help_${langCode }`}
                rows={4} onChange={updateCatalog} />
            </div>
          )
        } />

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

      <div className="card-footer">
        <div className="d-flex align-items-center gap-2">
          {catalog.id && <DeleteButton onClick={openDeleteModal} disabled={catalog.read_only} />}
          <BackButton className="ms-auto" />
          <SaveButton elementAction={elementAction} onClick={storeCatalog} disabled={catalog.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeCatalog} disabled={catalog.read_only} back={true} />
        </div>
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
