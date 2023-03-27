import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import MultiSelect from '../forms/MultiSelect'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import { BackButton, SaveButton, CreateButton, DeleteButton } from '../common/Buttons'

import QuestionInfo from '../info/QuestionInfo'
import DeleteQuestionModal from '../modals/DeleteQuestionModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditQuestion = ({ config, question, elements, elementActions}) => {

  const { parent, attributes, optionsets, options, conditions, pages, questionsets, widgetTypes, valueTypes } = elements

  const updateQuestion = (key, value) => elementActions.updateElement(question, {[key]: value})
  const storeQuestion = () => elementActions.storeElement('questions', question)
  const deleteQuestion = () => elementActions.deleteElement('questions', question)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <QuestionInfo question={question} elements={elements} />

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          {
            question.id ? <SaveButton onClick={storeQuestion} />
                        : <CreateButton onClick={storeQuestion} />
          }
        </div>
        {
          question.id ? <div>
            <strong>{gettext('Question')}{': '}</strong>
            <code className="code-questions">{question.uri}</code>
          </div> : <strong>{gettext('Create question')}</strong>
        }
      </div>

      {
        parent.page && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This question will be added to the page <code class="code-questions">%s</code>.'), [parent.page.uri])
          }} />
        </div>
      }
      {
        parent.questionset && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This question will be added to the question set <code class="code-questions">%s</code>.'), [parent.questionset.uri])
          }} />
        </div>
      }

      {
        question.id && <div className="panel-body panel-border">
          { info }
        </div>
      }

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={question} field="uri_prefix"
                  onChange={updateQuestion} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={question} field="uri_path"
                  onChange={updateQuestion} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={question} field="comment"
                      rows={4} onChange={updateQuestion} />
          </div>
          <div className="col-sm-12">
            <Checkbox config={config} element={question} field="locked"
                      onChange={updateQuestion} />
          </div>
          <div className="col-sm-12">
            <MultiSelect config={config} element={question} field="optionsets"
                         options={optionsets} verboseName="optionset"
                         onChange={updateQuestion} />
          </div>
          <div className="col-sm-12">
            <MultiSelect config={config} element={question} field="conditions"
                         options={conditions} verboseName="condition"
                         onChange={updateQuestion} />
          </div>
          <div className="col-sm-12">
            <Tabs id="#question-tabs" defaultActiveKey={0} animation={false}>

              <Tab className="pt-10" eventKey={0} title={gettext('General')}>
                <div className="row">
                  <div className="col-sm-12">
                    <Select config={config} element={question} field="attribute"
                            options={attributes} onChange={updateQuestion} />
                  </div>
                  <div className="col-sm-6">
                    <Checkbox config={config} element={question} field="is_collection"
                              onChange={updateQuestion} />
                  </div>
                  <div className="col-sm-6">
                    <Checkbox config={config} element={question} field="is_optional"
                              onChange={updateQuestion} />
                  </div>
                  <div className="col-sm-3">
                    <Select config={config} element={question} field="widget_type"
                            options={widgetTypes} onChange={updateQuestion} />
                  </div>
                  <div className="col-sm-3">
                    <Select config={config} element={question} field="value_type"
                            options={valueTypes} onChange={updateQuestion} />
                  </div>
                  <div className="col-sm-3">
                    <Text config={config} element={question} field="unit"
                          onChange={updateQuestion} />
                  </div>
                  <div className="col-sm-3">
                    <Text config={config} element={question} field="width"
                          onChange={updateQuestion} />
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
                          <Text config={config} element={question} field={`text_${lang_code }`}
                                onChange={updateQuestion} />
                        </div>
                        <div className="col-sm-12">
                          <Textarea config={config} element={question} field={`help_${lang_code }`}
                                    rows={4} onChange={updateQuestion} />
                        </div>
                        <div className="col-sm-6">
                          <Text config={config} element={question} field={`verbose_name_${lang_code }`}
                                onChange={updateQuestion} />
                        </div>
                        <div className="col-sm-6">
                          <Text config={config} element={question} field={`verbose_name_plural_${lang_code }`}
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
                          onChange={updateQuestion} />
                  </div>
                  <div className="col-sm-4">
                    <Text config={config} element={question} field="maximum"
                          onChange={updateQuestion} />
                  </div>
                  <div className="col-sm-4">
                    <Text config={config} element={question} field="step"
                          onChange={updateQuestion} />
                  </div>
                </div>
              </Tab>

              <Tab className="pt-10" eventKey={config.settings.languages.length + 2} title={gettext('Default')}>
                <div className="row">
                  <div className="col-sm-12">
                    {
                      config.settings && config.settings.languages.map(([lang_code, lang], index) => (
                        <Textarea key={index} config={config} element={question} field={`default_text_${lang_code }`}
                                  rows={2} onChange={updateQuestion} />
                      ))
                    }
                  </div>
                  <div className="col-sm-9">
                    <Select config={config} element={question} field="default_option"
                            options={options} onChange={updateQuestion} />
                  </div>
                  <div className="col-sm-3">
                    <Text config={config} element={question} field="default_external_id"
                          onChange={updateQuestion} />
                  </div>
                </div>
              </Tab>

            </Tabs>
          </div>
        </div>
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          {
            question.id ? <SaveButton onClick={storeQuestion} />
                        : <CreateButton onClick={storeQuestion} />
          }
        </div>
        {question.id && <DeleteButton onClick={openDeleteModal} />}
      </div>

      <DeleteQuestionModal question={question} info={info} show={showDeleteModal}
                           onClose={closeDeleteModal} onDelete={deleteQuestion} />
    </div>
  )
}

EditQuestion.propTypes = {
  config: PropTypes.object.isRequired,
  question: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default EditQuestion
