import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import Checkbox from '../forms/Checkbox'
import Select from '../forms/Select'
import UriPrefix from '../forms/UriPrefix'

import ElementHeading from '../common/ElementHeading'

const Question = ({ config, question, attributes, options, widgetTypes, valueTypes, warnings, errors, updateQuestion, storeQuestion }) => {
  return (
    <div className="panel panel-default">
      <ElementHeading verboseName={gettext('Question')} element={question} onSave={storeQuestion} />

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={question} field="uri_prefix"
                  warnings={warnings} errors={errors} onChange={updateQuestion} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={question} field="key"
                  warnings={warnings} errors={errors} onChange={updateQuestion} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={question} field="comment"
                      warnings={warnings} errors={errors} rows={4} onChange={updateQuestion} />
          </div>
          <div className="col-sm-12">
            <Checkbox config={config} element={question} field="locked"
                      warnings={warnings} errors={errors} onChange={updateQuestion} />
          </div>
          <div className="col-sm-12">
            <Tabs id="#question-tabs" defaultActiveKey={0} animation={false}>

              <Tab className="pt-10" eventKey={0} title={gettext('General')}>
                <div className="row">
                  <div className="col-sm-12">
                    <Select config={config} element={question} field="attribute"
                            warnings={warnings} errors={errors} options={attributes} onChange={updateQuestion} />
                  </div>
                  <div className="col-sm-6">
                    <Checkbox config={config} element={question} field="is_collection"
                              warnings={warnings} errors={errors} onChange={updateQuestion} />
                  </div>
                  <div className="col-sm-6">
                    <Checkbox config={config} element={question} field="is_optional"
                              warnings={warnings} errors={errors} onChange={updateQuestion} />
                  </div>
                  <div className="col-sm-3">
                    <Select config={config} element={question} field="widget_type"
                            warnings={warnings} errors={errors} options={widgetTypes} onChange={updateQuestion} />
                  </div>
                  <div className="col-sm-3">
                    <Select config={config} element={question} field="value_type"
                            warnings={warnings} errors={errors} options={valueTypes} onChange={updateQuestion} />
                  </div>
                  <div className="col-sm-3">
                    <Text config={config} element={question} field="unit"
                          warnings={warnings} errors={errors} onChange={updateQuestion} />
                  </div>
                  <div className="col-sm-3">
                    <Text config={config} element={question} field="width"
                          warnings={warnings} errors={errors} onChange={updateQuestion} />
                  </div>
                </div>
              </Tab>

              {
                config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                  const classNames = ''
                  return (
                    <Tab key={index} eventKey={index + 1} title={lang}>
                      <div className="row mt-10">
                        <div className="col-sm-12">
                          <Text config={config} element={question}
                                field={`text_${lang_code }`} warnings={warnings} errors={errors}
                                onChange={updateQuestion} />
                        </div>
                        <div className="col-sm-12">
                          <Textarea config={config} element={question}
                                    field={`help_${lang_code }`} warnings={warnings} errors={errors}
                                    rows={4} onChange={updateQuestion} />
                        </div>
                        <div className="col-sm-6">
                          <Text config={config} element={question}
                                field={`verbose_name_${lang_code }`} warnings={warnings} errors={errors}
                                onChange={updateQuestion} />
                        </div>
                        <div className="col-sm-6">
                          <Text config={config} element={question}
                                field={`verbose_name_plural_${lang_code }`} warnings={warnings} errors={errors}
                                onChange={updateQuestion} />
                        </div>
                      </div>
                    </Tab>
                  )
                })
              }

              <Tab className="pt-10" eventKey={config.settings.languages.length + 1} title={gettext('Range')}>
                <div className="row">
                  <div className="col-sm-4">
                    <Text config={config} element={question} field="minimum"
                          warnings={warnings} errors={errors} onChange={updateQuestion} />
                  </div>
                  <div className="col-sm-4">
                    <Text config={config} element={question} field="maximum"
                          warnings={warnings} errors={errors} onChange={updateQuestion} />
                  </div>
                  <div className="col-sm-4">
                    <Text config={config} element={question} field="step"
                          warnings={warnings} errors={errors} onChange={updateQuestion} />
                  </div>
                </div>
              </Tab>

              <Tab className="pt-10" eventKey={config.settings.languages.length + 2} title={gettext('Default')}>
                <div className="row">
                  <div className="col-sm-12">
                    {
                      config.settings && config.settings.languages.map(([lang_code, lang], index) => (
                        <Textarea key={index} config={config} element={question}
                                  field={`default_text_${lang_code }`} warnings={warnings} errors={errors}
                                  rows={2} onChange={updateQuestion} />
                      ))
                    }
                  </div>
                  <div className="col-sm-9">
                    <Select config={config} element={question} field="default_option"
                            warnings={warnings} errors={errors} options={options} onChange={updateQuestion} />
                  </div>
                  <div className="col-sm-3">
                    <Text config={config} element={question} field="default_external_id"
                          warnings={warnings} errors={errors} onChange={updateQuestion} />
                  </div>
                </div>
              </Tab>

            </Tabs>
          </div>
        </div>
      </div>
    </div>
  )
}

Question.propTypes = {
  config: PropTypes.object.isRequired,
  question: PropTypes.object.isRequired,
  attributes: PropTypes.array.isRequired,
  options: PropTypes.array.isRequired,
  widgetTypes: PropTypes.array.isRequired,
  valueTypes: PropTypes.array.isRequired,
  warnings: PropTypes.object,
  errors: PropTypes.object,
  updateQuestion: PropTypes.func.isRequired,
  storeQuestion: PropTypes.func.isRequired
}

export default Question
