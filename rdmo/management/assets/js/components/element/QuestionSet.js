import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import Checkbox from '../forms/Checkbox'
import Select from '../forms/Select'
import UriPrefix from '../forms/UriPrefix'

import ElementHeading from '../common/ElementHeading'

const QuestionSet = ({ config, questionset, updateQuestionSet, warnings, errors, storeQuestionSet }) => {
  return (
    <div className="panel panel-default">
      <ElementHeading verboseName={gettext('Question set')} element={questionset} onSave={storeQuestionSet} />

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={questionset} field="uri_prefix"
                  warnings={warnings} errors={errors} onChange={updateQuestionSet} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={questionset} field="key"
                  warnings={warnings} errors={errors} onChange={updateQuestionSet} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={questionset} field="comment"
                      warnings={warnings} errors={errors} rows={4} onChange={updateQuestionSet} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={questionset} field="locked"
                      warnings={warnings} errors={errors} onChange={updateQuestionSet} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={questionset} field="is_collection"
                      warnings={warnings} errors={errors} onChange={updateQuestionSet} />
          </div>
          <div className="col-sm-12">
            <Tabs id="#catalog-tabs" defaultActiveKey={0} animation={false}>
              {
                config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                  const classNames = ''
                  return (
                    <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                      <div className="row">
                        <div className="col-sm-12">
                          <Text config={config} element={questionset}
                                field={`title_${lang_code }`} warnings={warnings} errors={errors}
                                onChange={updateQuestionSet} />
                        </div>
                        <div className="col-sm-12">
                          <Textarea config={config} element={questionset}
                                    field={`help_${lang_code }`} warnings={warnings} errors={errors}
                                    rows={4} onChange={updateQuestionSet} />
                        </div>
                        <div className="col-sm-6">
                          <Text config={config} element={questionset}
                                field={`verbose_name_${lang_code }`} warnings={warnings} errors={errors}
                                onChange={updateQuestionSet} />
                        </div>
                        <div className="col-sm-6">
                          <Text config={config} element={questionset}
                                field={`verbose_name_plural_${lang_code }`} warnings={warnings} errors={errors}
                                onChange={updateQuestionSet} />
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

QuestionSet.propTypes = {
  config: PropTypes.object.isRequired,
  questionset: PropTypes.object.isRequired,
  warnings: PropTypes.object,
  errors: PropTypes.object,
  updateQuestionSet: PropTypes.func.isRequired,
  storeQuestionSet: PropTypes.func.isRequired
}

export default QuestionSet
