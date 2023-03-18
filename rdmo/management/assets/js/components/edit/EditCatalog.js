import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import OrderedMultiSelect from '../forms/OrderedMultiSelect'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import ElementButtons from '../common/ElementButtons'

const EditCatalog = ({ config, catalog, sites, groups, sections, updateElement, storeElement }) => {

  const updateCatalog = (key, value) => updateElement(catalog, key, value)
  const storeCatalog = () => storeElement('catalogs', catalog)

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons onSave={storeCatalog} />
        {
          catalog.id ? <div>
            <strong>{gettext('Catalog')}{': '}</strong>
            <code className="code-questions">{catalog.uri}</code>
          </div> : <strong>{gettext('Create catalog')}</strong>
        }
      </div>

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={catalog} field="uri_prefix" onChange={updateCatalog} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={catalog} field="uri_path" onChange={updateCatalog} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={catalog} field="comment" rows={4} onChange={updateCatalog} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={catalog} field="locked" onChange={updateCatalog} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={catalog} field="available" onChange={updateCatalog} />
          </div>
          <div className="col-sm-12">
            <OrderedMultiSelect config={config} element={catalog} field="sections"
                                options={sections} verboseName="section"
                                onChange={updateCatalog} />
          </div>
          <div className="col-sm-12">
            <Tabs id="#catalog-tabs" defaultActiveKey={0} animation={false}>
              {
                config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                  return (
                    <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                      <Text config={config} element={catalog} field={`title_${lang_code }`}
                            onChange={updateCatalog} />
                      <Textarea config={config} element={catalog} field={`help_${lang_code }`}
                                rows={4} onChange={updateCatalog} />
                    </Tab>
                  )
                })
              }
              <Tab className="pt-10" eventKey={config.settings.languages.length + 1} title={gettext('Visibility')}>
                <Select config={config} element={catalog} field="groups"
                        options={groups} onChange={updateCatalog} />
                <Select config={config} element={catalog} field="sites"
                        options={sites} onChange={updateCatalog} />
              </Tab>
            </Tabs>
          </div>
        </div>
      </div>
    </div>
  )
}

EditCatalog.propTypes = {
  config: PropTypes.object.isRequired,
  catalog: PropTypes.object.isRequired,
  sites: PropTypes.array.isRequired,
  groups: PropTypes.array.isRequired,
  sections: PropTypes.array.isRequired,
  storeElement: PropTypes.func.isRequired,
  updateElement: PropTypes.func.isRequired
}

export default EditCatalog
