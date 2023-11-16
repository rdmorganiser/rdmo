import React from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap'
import get from 'lodash/get'

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

const EditCatalog = ({ config, catalog, elements, elementActions }) => {

  const { sites, groups } = config
  const { elementAction, sections } = elements

  const updateCatalog = (key, value) => elementActions.updateElement(catalog, {[key]: value})
  const storeCatalog = (back) => elementActions.storeElement('catalogs', catalog, back)
  const deleteCatalog = () => elementActions.deleteElement('catalogs', catalog)

  const editSection = (value) => elementActions.fetchElement('sections', value.section)
  const createSection = () => elementActions.createElement('sections', { catalog } )

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <CatalogInfo catalog={catalog} elements={elements} />

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
            <UriPrefix config={config} element={catalog} field="uri_prefix" onChange={updateCatalog} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={catalog} field="uri_path" onChange={updateCatalog} />
          </div>
        </div>

        <Textarea config={config} element={catalog} field="comment" rows={4} onChange={updateCatalog} />

        <div className="row">
          <div className="col-sm-4">
            <Checkbox config={config} element={catalog} field="locked" onChange={updateCatalog} />
          </div>
          <div className="col-sm-4">
            <Checkbox config={config} element={catalog} field="available" onChange={updateCatalog} />
          </div>
          <div className="col-sm-4">
            <Number config={config} element={catalog} field="order" onChange={updateCatalog} />
          </div>
        </div>

        <Tabs id="#catalog-tabs" defaultActiveKey={0} animation={false}>
          {
            config.settings && config.settings.languages.map(([lang_code, lang], index) => (
              <Tab key={index} eventKey={index} title={lang}>
                <Text config={config} element={catalog} field={`title_${lang_code }`}
                      onChange={updateCatalog} />
                <Textarea config={config} element={catalog} field={`help_${lang_code }`}
                          rows={4} onChange={updateCatalog} />
              </Tab>
            ))
          }
        </Tabs>

        <OrderedMultiSelect config={config} element={catalog} field="sections" options={sections}
                            addText={gettext('Add existing section')} createText={gettext('Create new section')}
                            onChange={updateCatalog} onCreate={createSection} onEdit={editSection} />

        {get(config, 'settings.groups') && <Select config={config} element={catalog} field="groups"
                                                   options={groups} onChange={updateCatalog} isMulti />}

        {get(config, 'settings.multisite') && <Select config={config} element={catalog} field="sites"
                                                      options={sites} onChange={updateCatalog} isMulti />}

        {get(config, 'settings.multisite') && <Select config={config} element={catalog} field="editors"
                                                      options={sites} onChange={updateCatalog} isMulti />}
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
  config: PropTypes.object.isRequired,
  catalog: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default EditCatalog
