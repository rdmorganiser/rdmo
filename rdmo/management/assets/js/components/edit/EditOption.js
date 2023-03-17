import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import ElementButtons from '../common/ElementButtons'

const EditOption = ({ config, option, updateElement, storeElement }) => {

  const updateOption = (key, value) => updateElement(option, key, value)
  const storeOption = () => storeElement('options', option)

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons onSave={storeOption} />
        <strong>{gettext('Option')}{': '}</strong>
        <code className="code-options">{option.uri}</code>
      </div>

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={option} field="uri_prefix"
                       onChange={updateOption} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={option} field="uri_path"
                  onChange={updateOption} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={option} field="comment"
                      rows={4} onChange={updateOption} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={option} field="locked"
                      onChange={updateOption} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={option} field="additional_input"
                      onChange={updateOption} />
          </div>
          <div className="col-sm-12">
            <Tabs id="#option-tabs" defaultActiveKey={0} animation={false}>
              {
                config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                  return (
                    <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                      <div className="row">
                        <div className="col-sm-12">
                          <Text config={config} element={option} field={`text_${lang_code }`}
                                onChange={updateOption} />
                        </div>
                      </div>
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

EditOption.propTypes = {
  config: PropTypes.object.isRequired,
  option: PropTypes.object.isRequired,
  storeElement: PropTypes.func.isRequired,
  updateElement: PropTypes.func.isRequired
}

export default EditOption
