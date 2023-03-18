import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import OrderedMultiSelect from '../forms/OrderedMultiSelect'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import ElementButtons from '../common/ElementButtons'

const EditQuestionSet = ({ config, questionset, attributes, conditions,
                           questionsets, questions, updateElement, storeElement }) => {

  const updateQuestionSet = (key, value) => updateElement(questionset, key, value)
  const storeQuestionSet = () => storeElement('questionsets', questionset)

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons onSave={storeQuestionSet} />
        {
          questionset.id ? <div>
            <strong>{gettext('Question set')}{': '}</strong>
            <code className="code-questions">{questionset.uri}</code>
          </div> : <strong>{gettext('Create question set')}</strong>
        }
      </div>

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={questionset} field="uri_prefix"
                  onChange={updateQuestionSet} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={questionset} field="uri_path"
                  onChange={updateQuestionSet} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={questionset} field="comment"
                      rows={4} onChange={updateQuestionSet} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={questionset} field="locked"
                      onChange={updateQuestionSet} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={questionset} field="is_collection"
                      onChange={updateQuestionSet} />
          </div>
          <div className="col-sm-12">
            <Select config={config} element={questionset} field="attribute"
                    options={attributes} onChange={updateQuestionSet} />
          </div>
          <div className="col-sm-12">
            <OrderedMultiSelect config={config} element={questionset} field="questionsets"
                                options={questionsets} verboseName="questionset"
                                onChange={updateQuestionSet} />
          </div>
          <div className="col-sm-12">
            <OrderedMultiSelect config={config} element={questionset} field="questions"
                                options={questions}  verboseName="question"
                                onChange={updateQuestionSet} />
          </div>
          <div className="col-sm-12">
            <Tabs id="#catalog-tabs" defaultActiveKey={0} animation={false}>
              {
                config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                  return (
                    <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                      <div className="row">
                        <div className="col-sm-12">
                          <Text config={config} element={questionset} field={`title_${lang_code }`}
                                onChange={updateQuestionSet} />
                        </div>
                        <div className="col-sm-12">
                          <Textarea config={config} element={questionset} field={`help_${lang_code }`}
                                    rows={4} onChange={updateQuestionSet} />
                        </div>
                        <div className="col-sm-6">
                          <Text config={config} element={questionset} field={`verbose_name_${lang_code }`}
                                onChange={updateQuestionSet} />
                        </div>
                        <div className="col-sm-6">
                          <Text config={config} element={questionset} field={`verbose_name_plural_${lang_code }`}
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

EditQuestionSet.propTypes = {
  config: PropTypes.object.isRequired,
  questionset: PropTypes.object.isRequired,
  questionsets: PropTypes.array,
  questions: PropTypes.array,
  storeElement: PropTypes.func.isRequired,
  updateElement: PropTypes.func.isRequired
}

export default EditQuestionSet
