import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import Checkbox from '../forms/Checkbox'
import Select from '../forms/Select'
import UriPrefix from '../forms/UriPrefix'

const Question = ({ config, question, attributes, options, widgetTypes, valueTypes, warnings, errors, updateQuestion, storeQuestion }) => {
  return (
    <div>
      <div className="panel panel-default">
        <div className="panel-heading">
          <div className="pull-right">
            <button className="btn btn-xs btn-default" onClick={event => history.back()}>
              {gettext('Back')}
            </button>
            {' '}
            <button className="btn btn-xs btn-primary" onClick={event => storeQuestion()}>
              {gettext('Save')}
            </button>
          </div>
          <div>
            <strong>{gettext('Question')}</strong>
          </div>
        </div>
        <div className="panel-body">
          <code className="code-questions">{question.uri}</code>
        </div>
      </div>

      <div className="row">
        <div className="col-sm-6">
          <UriPrefix config={config} element={question} elementType="questions" field="uri_prefix"
                warnings={warnings} errors={errors} onChange={updateQuestion} />
        </div>
        <div className="col-sm-6">
          <Text config={config} element={question} elementType="questions" field="key"
                warnings={warnings} errors={errors} onChange={updateQuestion} />
        </div>
        <div className="col-sm-12">
          <Textarea config={config} element={question} elementType="questions" field="comment"
                    warnings={warnings} errors={errors} rows={4} onChange={updateQuestion} />
        </div>
        <div className="col-sm-12">
          <Checkbox config={config} element={question} elementType="questions" field="locked"
                    warnings={warnings} errors={errors} onChange={updateQuestion} />
        </div>
        <div className="col-sm-12">
          <Tabs id="#question-tabs" defaultActiveKey={0} animation={false}>

            <Tab className="pt-10" eventKey={0} title={gettext('General')}>
              <div className="row">
                <div className="col-sm-12">
                  <Select config={config} element={question} elementType="questions" field="attribute"
                          warnings={warnings} errors={errors} options={attributes} onChange={updateQuestion} />
                </div>
                <div className="col-sm-6">
                  <Checkbox config={config} element={question} elementType="questions" field="is_collection"
                            warnings={warnings} errors={errors} onChange={updateQuestion} />
                </div>
                <div className="col-sm-6">
                  <Checkbox config={config} element={question} elementType="questions" field="is_optional"
                            warnings={warnings} errors={errors} onChange={updateQuestion} />
                </div>
                <div className="col-sm-3">
                  <Select config={config} element={question} elementType="questions" field="widget_type"
                          warnings={warnings} errors={errors} options={widgetTypes} onChange={updateQuestion} />
                </div>
                <div className="col-sm-3">
                  <Select config={config} element={question} elementType="questions" field="value_type"
                          warnings={warnings} errors={errors} options={valueTypes} onChange={updateQuestion} />
                </div>
                <div className="col-sm-3">
                  <Text config={config} element={question} elementType="questions" field="unit"
                        warnings={warnings} errors={errors} onChange={updateQuestion} />
                </div>
                <div className="col-sm-3">
                  <Text config={config} element={question} elementType="questions" field="width"
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
                        <Text config={config} element={question} elementType="questions"
                              field={`text_${lang_code }`} warnings={warnings} errors={errors}
                              onChange={updateQuestion} />
                      </div>
                      <div className="col-sm-12">
                        <Textarea config={config} element={question} elementType="questions"
                                  field={`help_${lang_code }`} warnings={warnings} errors={errors}
                                  rows={4} onChange={updateQuestion} />
                      </div>
                      <div className="col-sm-6">
                        <Text config={config} element={question} elementType="questions"
                              field={`verbose_name_${lang_code }`} warnings={warnings} errors={errors}
                              onChange={updateQuestion} />
                      </div>
                      <div className="col-sm-6">
                        <Text config={config} element={question} elementType="questions"
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
                  <Text config={config} element={question} elementType="questions" field="minimum"
                        warnings={warnings} errors={errors} onChange={updateQuestion} />
                </div>
                <div className="col-sm-4">
                  <Text config={config} element={question} elementType="questions" field="maximum"
                        warnings={warnings} errors={errors} onChange={updateQuestion} />
                </div>
                <div className="col-sm-4">
                  <Text config={config} element={question} elementType="questions" field="step"
                        warnings={warnings} errors={errors} onChange={updateQuestion} />
                </div>
              </div>
            </Tab>

            <Tab className="pt-10" eventKey={config.settings.languages.length + 2} title={gettext('Default')}>
              <div className="row">
                <div className="col-sm-12">
                  {
                    config.settings && config.settings.languages.map(([lang_code, lang], index) => (
                      <Textarea key={index} config={config} element={question} elementType="questions"
                                field={`default_text_${lang_code }`} warnings={warnings} errors={errors}
                                rows={2} onChange={updateQuestion} />
                    ))
                  }
                </div>
                <div className="col-sm-9">
                  <Select config={config} element={question} elementType="questions" field="default_option"
                          warnings={warnings} errors={errors} options={options} onChange={updateQuestion} />
                </div>
                <div className="col-sm-3">
                  <Text config={config} element={question} elementType="questions" field="default_external_id"
                        warnings={warnings} errors={errors} onChange={updateQuestion} />
                </div>
              </div>
            </Tab>

          </Tabs>
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
