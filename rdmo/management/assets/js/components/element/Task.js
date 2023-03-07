import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Number from '../forms/Number'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import ElementHeading from '../common/ElementHeading'

const Task = ({ config, task, warnings, errors, updateTask, storeTask,
                attributes, catalogs, sites, groups }) => {
  return (
    <div className="panel panel-default">
      <ElementHeading verboseName={gettext('Task')} element={task} onSave={storeTask} />

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={task} field="uri_prefix"
                       warnings={warnings} errors={errors} onChange={updateTask} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={task} field="key"
                  warnings={warnings} errors={errors} onChange={updateTask} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={task} field="comment"
                      warnings={warnings} errors={errors} rows={4} onChange={updateTask} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={task} field="locked"
                      warnings={warnings} errors={errors} onChange={updateTask} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={task} field="available"
                      warnings={warnings} errors={errors} onChange={updateTask} />
          </div>

          <div className="col-sm-12">
            <Tabs id="#task-tabs" defaultActiveKey={0} animation={false}>
              {
                config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                  const classNames = ''
                  return (
                    <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                      <Text config={config} element={task} field={`title_${lang_code }`}
                            warnings={warnings} errors={errors} onChange={updateTask} />
                      <Textarea config={config} element={task} field={`text_${lang_code }`}
                                warnings={warnings} errors={errors} rows={8} onChange={updateTask} />
                    </Tab>
                  )
                })
              }
              <Tab className="pt-10" eventKey={config.settings.languages.length + 1} title={gettext('Time frame')}>
                <div className="row">
                  <div className="col-sm-12">
                    <Select config={config} element={task} field="start_attribute"
                            warnings={warnings} errors={errors} options={attributes} onChange={updateTask} />
                  </div>
                  <div className="col-sm-12">
                    <Select config={config} element={task} field="end_attribute"
                            warnings={warnings} errors={errors} options={attributes} onChange={updateTask} />
                  </div>
                  <div className="col-sm-6">
                    <Number config={config} element={task} field="days_before"
                             warnings={warnings} errors={errors} onChange={updateTask} />
                  </div>
                  <div className="col-sm-6">
                    <Number config={config} element={task} field="days_after"
                             warnings={warnings} errors={errors} onChange={updateTask} />
                  </div>
                </div>
              </Tab>
              <Tab className="pt-10" eventKey={config.settings.languages.length + 2} title={gettext('Visibility')}>
                <Select config={config} element={task} field="catalogs"
                        warnings={warnings} errors={errors} options={catalogs} onChange={updateTask} />
                <Select config={config} element={task} field="groups"
                        warnings={warnings} errors={errors} options={groups} onChange={updateTask} />
                <Select config={config} element={task} field="sites"
                        warnings={warnings} errors={errors} options={sites} onChange={updateTask} />
              </Tab>
            </Tabs>
          </div>
        </div>
      </div>
    </div>
  )
}

Task.propTypes = {
  config: PropTypes.object.isRequired,
  task: PropTypes.object.isRequired,
  warnings: PropTypes.object.isRequired,
  errors: PropTypes.object.isRequired,
  updateTask: PropTypes.func.isRequired,
  storeTask: PropTypes.func.isRequired,
  attributes: PropTypes.array,
  catalogs: PropTypes.array,
  groups: PropTypes.array,
  sites: PropTypes.array
}

export default Task
