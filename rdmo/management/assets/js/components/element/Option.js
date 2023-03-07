import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import ElementHeading from '../common/ElementHeading'

const Option = ({ config, option, warnings, errors, updateOption, storeOption }) => {
  return (
    <div className="panel panel-default">
      <ElementHeading verboseName={gettext('Option')} element={option} onSave={storeOption} />

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={option} field="uri_prefix"
                       warnings={warnings} errors={errors} onChange={updateOption} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={option} field="key"
                  warnings={warnings} errors={errors} onChange={updateOption} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={option} field="comment"
                      warnings={warnings} errors={errors} rows={4} onChange={updateOption} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={option} field="locked"
                      warnings={warnings} errors={errors} onChange={updateOption} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={option} field="additional_input"
                      warnings={warnings} errors={errors} onChange={updateOption} />
          </div>
          <div className="col-sm-12">
            <Tabs id="#option-tabs" defaultActiveKey={0} animation={false}>
              {
                config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                  return (
                    <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                      <div className="row">
                        <div className="col-sm-12">
                          <Text config={config} element={option}
                                field={`text_${lang_code }`} warnings={warnings} errors={errors}
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

Option.propTypes = {
  config: PropTypes.object.isRequired,
  option: PropTypes.object.isRequired,
  warnings: PropTypes.object.isRequired,
  errors: PropTypes.object.isRequired,
  updateOption: PropTypes.func.isRequired,
  storeOption: PropTypes.func.isRequired
}

export default Option
