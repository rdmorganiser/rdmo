import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import CodeMirror from '../forms/CodeMirror'
import Checkbox from '../forms/Checkbox'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import ElementHeading from '../common/ElementHeading'

const View = ({ config, view, warnings, errors, updateView, storeView,
                catalogs, sites, groups }) => {
  return (
    <div className="panel panel-default">
      <ElementHeading verboseName={gettext('View')} element={view} onSave={storeView} />

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={view} field="uri_prefix"
                       warnings={warnings} errors={errors} onChange={updateView} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={view} field="key"
                  warnings={warnings} errors={errors} onChange={updateView} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={view} field="comment"
                      warnings={warnings} errors={errors} rows={4} onChange={updateView} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={view} field="locked"
                      warnings={warnings} errors={errors} onChange={updateView} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={view} field="available"
                      warnings={warnings} errors={errors} onChange={updateView} />
          </div>
          <div className="col-sm-12">
            <CodeMirror config={config} element={view} field="template"
                        warnings={warnings} errors={errors} onChange={updateView} />
          </div>
          <div className="col-sm-12">
            <Tabs id="#view-tabs" defaultActiveKey={0} animation={false}>
              {
                config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                  return (
                    <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                      <Text config={config} element={view} field={`title_${lang_code }`}
                            warnings={warnings} errors={errors} onChange={updateView} />
                      <Textarea config={config} element={view} field={`help_${lang_code }`}
                                warnings={warnings} errors={errors} rows={8} onChange={updateView} />
                    </Tab>
                  )
                })
              }
              <Tab className="pt-10" eventKey={config.settings.languages.length + 1} title={gettext('Visibility')}>
                <Select config={config} element={view} field="catalogs"
                        warnings={warnings} errors={errors} options={catalogs} onChange={updateView} />
                <Select config={config} element={view} field="groups"
                        warnings={warnings} errors={errors} options={groups} onChange={updateView} />
                <Select config={config} element={view} field="sites"
                        warnings={warnings} errors={errors} options={sites} onChange={updateView} />
              </Tab>
            </Tabs>
          </div>
        </div>
      </div>
    </div>
  )
}

View.propTypes = {
  config: PropTypes.object.isRequired,
  view: PropTypes.object.isRequired,
  warnings: PropTypes.object.isRequired,
  errors: PropTypes.object.isRequired,
  updateView: PropTypes.func.isRequired,
  storeView: PropTypes.func.isRequired,
  catalogs: PropTypes.array,
  groups: PropTypes.array,
  sites: PropTypes.array
}

export default View
