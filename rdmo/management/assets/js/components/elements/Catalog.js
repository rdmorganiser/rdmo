import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import { getLabel, getHelp } from 'rdmo/management/assets/js/utils/meta'


const Catalog = ({ config, catalog, warnings, errors, updateCatalog, storeCatalog }) => {
  return (
    <div>
      <div className="panel panel-default">
        <div className="panel-heading">
          <div className="pull-right">
            <button className="btn btn-xs btn-default" onClick={event => history.back()}>
              {gettext('Back')}
            </button>
            {' '}
            <button className="btn btn-xs btn-primary" onClick={event => storeCatalog()}>
              {gettext('Save')}
            </button>
          </div>
          <div>
            <strong>{gettext('Catalog')}</strong>
          </div>
        </div>
        <div className="panel-body">
          <code className="code-questions">{catalog.uri}</code>
        </div>
      </div>

      <div className="row">
        <div className="col-sm-6">
          <UriPrefix config={config} element={catalog} elementType="catalogs" field="uri_prefix"
                     warnings={warnings} errors={errors} onChange={updateCatalog} />
        </div>
        <div className="col-sm-6">
          <Text config={config} element={catalog} elementType="catalogs" field="key"
                warnings={warnings} errors={errors} onChange={updateCatalog} />
        </div>
        <div className="col-sm-12">
          <Textarea config={config} element={catalog} elementType="catalogs" field="comment"
                    warnings={warnings} errors={errors} rows={4} onChange={updateCatalog} />
        </div>
        <div className="col-sm-12">
          <Checkbox config={config} element={catalog} elementType="catalogs" field="locked"
                    warnings={warnings} errors={errors} onChange={updateCatalog} />
        </div>
        <div className="col-sm-12">
          <Tabs id="#catalog-tabs" defaultActiveKey={0} animation={false}>
            <Tab className="pt-10" eventKey={0} title={gettext('General')}>
              <Checkbox config={config} element={catalog} elementType="catalogs" field="available"
                        warnings={warnings} errors={errors} onChange={updateCatalog} />
            </Tab>
            {
              config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                const classNames = ''
                return (
                  <Tab className="pt-10" key={index} eventKey={index + 1} title={lang}>
                    <Text config={config} element={catalog} elementType="catalogs" field={`title_${lang_code }`}
                          warnings={warnings} errors={errors} onChange={updateCatalog} />
                    <Textarea config={config} element={catalog} elementType="catalogs" field={`help_${lang_code }`}
                              warnings={warnings} errors={errors} rows={4} onChange={updateCatalog} />
                  </Tab>
                )
              })
            }
          </Tabs>
        </div>
      </div>
    </div>
  )
}

Catalog.propTypes = {
  config: PropTypes.object.isRequired,
  catalog: PropTypes.object.isRequired,
  warnings: PropTypes.object,
  errors: PropTypes.object,
  updateCatalog: PropTypes.func.isRequired,
  storeCatalog: PropTypes.func.isRequired
}

export default Catalog
