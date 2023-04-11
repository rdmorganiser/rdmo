import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import MultiSelect from '../forms/MultiSelect'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'

import QuestionInfo from '../info/QuestionInfo'
import DeleteQuestionModal from '../modals/DeleteQuestionModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditQuestion = ({ config, question, elements, elementActions}) => {

  const { parent, attributes, optionsets, options, conditions, pages, questionsets, widgetTypes, valueTypes } = elements

  const updateQuestion = (key, value) => elementActions.updateElement(question, {[key]: value})
  const storeQuestion = (back) => elementActions.storeElement('questions', question, back)
  const deleteQuestion = () => elementActions.deleteElement('questions', question)

  const editOptionSet = (optionset) => elementActions.fetchElement('optionsets', optionset)
  const createOptionSet = () => elementActions.createElement('optionsets', { question })

  const editCondition = (condition) => elementActions.fetchElement('conditions', condition)
  const createCondition = () => elementActions.createElement('conditions', { question })

  const editAttribute = (attribute) => elementActions.fetchElement('attributes', attribute)
  const createAttribute = () => elementActions.createElement('attributes', { question })

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <QuestionInfo question={question} elements={elements} elementActions={elementActions} />

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <SaveButton element={question} onClick={storeQuestion} />
          <SaveButton element={question} onClick={storeQuestion} back={true}/>
        </div>
        {
          question.id ? <>
            <strong>{gettext('Question')}{': '}</strong>
            <code className="code-questions">{question.uri}</code>
          </> : <strong>{gettext('Create question')}</strong>
        }
      </div>

      {
        parent && parent.page && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This question will be added to the page <code class="code-questions">%s</code>.'), [parent.page.uri])
          }} />
        </div>
      }
      {
        parent && parent.questionset && <div className="panel-body panel-border">
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
        </div>

        <Textarea config={config} element={question} field="comment"
                  rows={4} onChange={updateQuestion} />

        <div className="row">
          <div className="col-sm-4">
            <Checkbox config={config} element={question} field="locked"
                      onChange={updateQuestion} />
          </div>
          <div className="col-sm-4">
            <Checkbox config={config} element={question} field="is_collection"
                      onChange={updateQuestion} />
          </div>
          <div className="col-sm-4">
            <Checkbox config={config} element={question} field="is_optional"
                      onChange={updateQuestion} />
          </div>
        </div>

        <Tabs id="#question-tabs" defaultActiveKey={0} animation={false}>
          {
            config.settings && config.settings.languages.map(([lang_code, lang], index) => {
              return (
                <Tab key={index} eventKey={index} title={lang}>
                  <Text config={config} element={question} field={`text_${lang_code }`}
                        onChange={updateQuestion} />

                  <Textarea config={config} element={question} field={`help_${lang_code }`}
                            rows={8} onChange={updateQuestion} />

                  <div className="row">
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
        </Tabs>

        <Select config={config} element={question} field="attribute" verboseName={gettext('attribute')}
                options={attributes} onChange={updateQuestion} onCreate={createAttribute} onEdit={editAttribute} />

        <div className="row">
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

        <MultiSelect config={config} element={question} field="optionsets"
                     options={optionsets} verboseName="optionset"
                     onChange={updateQuestion} onCreate={createOptionSet} onEdit={editOptionSet} />

        <MultiSelect config={config} element={question} field="conditions"
                     options={conditions} verboseName="condition"
                     onChange={updateQuestion} onCreate={createCondition} onEdit={editCondition} />

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

        <Tabs id="#question-default-tabs" defaultActiveKey={0} animation={false}>
          {
            config.settings && config.settings.languages.map(([lang_code, lang], index) => (
              <Tab key={index} eventKey={index} title={lang}>
                <Textarea key={index} config={config} element={question} field={`default_text_${lang_code }`}
                          rows={2} onChange={updateQuestion} />
              </Tab>
            ))
          }
        </Tabs>

        <div className="row">
          <div className="col-sm-6">
            <Select config={config} element={question} field="default_option"
                    options={options} onChange={updateQuestion} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={question} field="default_external_id"
                  onChange={updateQuestion} />
          </div>
        </div>
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton element={question} onClick={storeQuestion} />
          <SaveButton element={question} onClick={storeQuestion} back={true}/>
        </div>
        <DeleteButton element={question} onClick={openDeleteModal} />
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
