import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Number from '../forms/Number'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import ElementButtons from '../common/ElementButtons'

const EditTask = ({ config, task, attributes, catalogs, sites, groups,
                    updateElement, storeElement }) => {

  const updateTask = (key, value) => updateElement(task, key, value)
  const storeTask = () => storeElement('tasks', task)

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons onSave={storeTask} />
        <strong>{gettext('Task')}{': '}</strong>
        <code className="code-tasks">{task.uri}</code>
      </div>

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={task} field="uri_prefix"
                       onChange={updateTask} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={task} field="key"
                  onChange={updateTask} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={task} field="comment"
                      rows={4} onChange={updateTask} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={task} field="locked"
                      onChange={updateTask} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={task} field="available"
                      onChange={updateTask} />
          </div>

          <div className="col-sm-12">
            <Tabs id="#task-tabs" defaultActiveKey={0} animation={false}>
              {
                config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                  const classNames = ''
                  return (
                    <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                      <Text config={config} element={task} field={`title_${lang_code }`}
                            onChange={updateTask} />
                      <Textarea config={config} element={task} field={`text_${lang_code }`}
                                rows={8} onChange={updateTask} />
                    </Tab>
                  )
                })
              }
              <Tab className="pt-10" eventKey={config.settings.languages.length + 1} title={gettext('Time frame')}>
                <div className="row">
                  <div className="col-sm-12">
                    <Select config={config} element={task} field="start_attribute"
                            options={attributes} onChange={updateTask} />
                  </div>
                  <div className="col-sm-12">
                    <Select config={config} element={task} field="end_attribute"
                            options={attributes} onChange={updateTask} />
                  </div>
                  <div className="col-sm-6">
                    <Number config={config} element={task} field="days_before"
                             onChange={updateTask} />
                  </div>
                  <div className="col-sm-6">
                    <Number config={config} element={task} field="days_after"
                             onChange={updateTask} />
                  </div>
                </div>
              </Tab>
              <Tab className="pt-10" eventKey={config.settings.languages.length + 2} title={gettext('Visibility')}>
                <Select config={config} element={task} field="catalogs"
                        options={catalogs} onChange={updateTask} />
                <Select config={config} element={task} field="groups"
                        options={groups} onChange={updateTask} />
                <Select config={config} element={task} field="sites"
                        options={sites} onChange={updateTask} />
              </Tab>
            </Tabs>
          </div>
        </div>
      </div>
    </div>
  )
}

EditTask.propTypes = {
  config: PropTypes.object.isRequired,
  task: PropTypes.object.isRequired,
  attributes: PropTypes.array,
  catalogs: PropTypes.array,
  groups: PropTypes.array,
  sites: PropTypes.array,
  storeElement: PropTypes.func.isRequired,
  updateElement: PropTypes.func.isRequired
}

export default EditTask
