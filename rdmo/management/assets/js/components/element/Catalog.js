import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import OrderedMultiSelect from '../forms/OrderedMultiSelect'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import ElementHeading from '../common/ElementHeading'

const Catalog = ({ config, catalog, sections, warnings, errors, updateCatalog, storeCatalog }) => {
  return (
    <div className="panel panel-default">
      <ElementHeading verboseName={gettext('Catalog')} element={catalog} onSave={storeCatalog} />

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={catalog} field="uri_prefix"
                       warnings={warnings} errors={errors} onChange={updateCatalog} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={catalog} field="key"
                  warnings={warnings} errors={errors} onChange={updateCatalog} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={catalog} field="comment"
                      warnings={warnings} errors={errors} rows={4} onChange={updateCatalog} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={catalog} field="locked"
                      warnings={warnings} errors={errors} onChange={updateCatalog} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={catalog} field="available"
                      warnings={warnings} errors={errors} onChange={updateCatalog} />
          </div>
          <div className="col-sm-12">
            <OrderedMultiSelect config={config} element={catalog} field="sections" selectField="section"
                                options={sections} warnings={warnings} errors={errors}
                                onChange={updateCatalog} />
          </div>
          <div className="col-sm-12">
            <Tabs id="#catalog-tabs" defaultActiveKey={0} animation={false}>
              {
                config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                  const classNames = ''
                  return (
                    <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                      <Text config={config} element={catalog} field={`title_${lang_code }`}
                            warnings={warnings} errors={errors} onChange={updateCatalog} />
                      <Textarea config={config} element={catalog} field={`help_${lang_code }`}
                                warnings={warnings} errors={errors} rows={4} onChange={updateCatalog} />
                    </Tab>
                  )
                })
              }
            </Tabs>
          </div>
        </div>
      </div>
    </div>
  )
}

Catalog.propTypes = {
  config: PropTypes.object.isRequired,
  catalog: PropTypes.object.isRequired,
  sections: PropTypes.array,
  warnings: PropTypes.object,
  errors: PropTypes.object,
  updateCatalog: PropTypes.func.isRequired,
  storeCatalog: PropTypes.func.isRequired
}

export default Catalog
