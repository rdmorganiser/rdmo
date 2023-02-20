import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import Checkbox from '../forms/Checkbox'
import Select from '../forms/Select'
import UriPrefix from '../forms/UriPrefix'

const QuestionSet = ({ config, questionset, updateQuestionSet, warnings, errors, storeQuestionSet }) => {
  return (
    <div>
      <div className="panel panel-default">
        <div className="panel-heading">
          <div className="pull-right">
            <button className="btn btn-xs btn-default" onClick={event => history.back()}>
              {gettext('Back')}
            </button>
            {' '}
            <button className="btn btn-xs btn-primary" onClick={event => storeQuestionSet()}>
              {gettext('Save')}
            </button>
          </div>
          <div>
            <strong>{gettext('Question set')}</strong>
          </div>
        </div>
        <div className="panel-body">
          <code className="code-questions">{questionset.uri}</code>
        </div>
      </div>

      <div className="row">
        <div className="col-sm-6">
          <UriPrefix config={config} element={questionset} elementType="questionsets" field="uri_prefix"
                warnings={warnings} errors={errors} onChange={updateQuestionSet} />
        </div>
        <div className="col-sm-6">
          <Text config={config} element={questionset} elementType="questionsets" field="key"
                warnings={warnings} errors={errors} onChange={updateQuestionSet} />
        </div>
        <div className="col-sm-12">
          <Textarea config={config} element={questionset} elementType="questionsets" field="comment"
                    warnings={warnings} errors={errors} rows={4} onChange={updateQuestionSet} />
        </div>
        <div className="col-sm-12">
          <Checkbox config={config} element={questionset} elementType="questionsets" field="locked"
                    warnings={warnings} errors={errors} onChange={updateQuestionSet} />
        </div>
        <div className="col-sm-12">
          <Tabs id="#catalog-tabs" defaultActiveKey={0} animation={false}>
            <Tab className="pt-10" eventKey={0} title={gettext('General')}>
              <Checkbox config={config} element={questionset} elementType="questionsets" field="is_collection"
                        warnings={warnings} errors={errors} onChange={updateQuestionSet} />
            </Tab>
            {
              config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                const classNames = ''
                return (
                  <Tab className="pt-10" key={index} eventKey={index + 1} title={lang}>
                    <div className="row">
                      <div className="col-sm-12">
                        <Text config={config} element={questionset} elementType="questionsets"
                              field={`title_${lang_code }`} warnings={warnings} errors={errors}
                              onChange={updateQuestionSet} />
                      </div>
                      <div className="col-sm-12">
                        <Textarea config={config} element={questionset} elementType="questionsets"
                                  field={`help_${lang_code }`} warnings={warnings} errors={errors}
                                  rows={4} onChange={updateQuestionSet} />
                      </div>
                      <div className="col-sm-6">
                        <Text config={config} element={questionset} elementType="questionsets"
                              field={`verbose_name_${lang_code }`} warnings={warnings} errors={errors}
                              onChange={updateQuestionSet} />
                      </div>
                      <div className="col-sm-6">
                        <Text config={config} element={questionset} elementType="questionsets"
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
