import React, { Component, useState } from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';
import isUndefined from 'lodash/isUndefined'
import orderBy from 'lodash/orderBy'

import Checkbox from '../forms/Checkbox'
import OrderedMultiSelect from '../forms/OrderedMultiSelect'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import { BackButton, SaveButton, CreateButton, DeleteButton } from '../common/Buttons'

import QuestionSetInfo from '../info/QuestionSetInfo'
import DeleteQuestionSetModal from '../modals/DeleteQuestionSetModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditQuestionSet = ({ config, questionset, elements, elementActions }) => {

  const { parent, attributes, conditions, pages, questionsets, questions } = elements

  const elementValues = orderBy(questionset.questions.concat(questionset.questionsets), ['order', 'uri'])
  const elementOptions = elements.questions.map(question => ({
    value: 'question-' + question.id,
    label: interpolate(gettext('Question: %s'), [question.uri])
  })).concat(elements.questionsets.map(questionset => ({
    value: 'questionset-' + questionset.id,
    label: interpolate(gettext('Question set: %s'), [questionset.uri])
  })))

  const updateQuestionSet = (key, value) => {
    if (key == 'elements') {
      elementActions.updateElement(questionset, {
        questions: value.filter(e => !isUndefined(e.question)),
        questionsets: value.filter(e => !isUndefined(e.questionset))
      })
    } else {
      elementActions.updateElement(questionset, { [key]: value })
    }
  }
  const storeQuestionSet = () => elementActions.storeElement('questionsets', questionset)
  const deleteQuestionSet = () => elementActions.deleteElement('questionsets', questionset)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <QuestionSetInfo questionset={questionset} elements={elements} />

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          {
            questionset.id ? <SaveButton onClick={storeQuestionSet} />
                           : <CreateButton onClick={storeQuestionSet} />
          }
        </div>
        {
          questionset.id ? <div>
            <strong>{gettext('Question set')}{': '}</strong>
            <code className="code-questions">{questionset.uri}</code>
          </div> : <strong>{gettext('Create question set')}</strong>
        }
      </div>

      {
        parent.page && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This question set will be added to the page <code class="code-questions">%s</code>.'), [parent.page.uri])
          }} />
        </div>
      }
      {
        parent.questionset && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This question set will be added to the question set <code class="code-questions">%s</code>.'), [parent.questionset.uri])
          }} />
        </div>
      }

      {
        questionset.id && <div className="panel-body panel-border">
          { info }
        </div>
      }

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
            <OrderedMultiSelect config={config} element={questionset} field="elements"
                                values={elementValues} options={elementOptions}
                                verboseName={gettext('element')}
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

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          {
            questionset.id ? <SaveButton onClick={storeQuestionSet} />
                           : <CreateButton onClick={storeQuestionSet} />
          }
        </div>
        {questionset.id && <DeleteButton onClick={openDeleteModal} />}
      </div>

      <DeleteQuestionSetModal questionset={questionset} info={info} show={showDeleteModal}
                              onClose={closeDeleteModal} onDelete={deleteQuestionSet} />
    </div>
  )
}

EditQuestionSet.propTypes = {
  config: PropTypes.object.isRequired,
  questionset: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default EditQuestionSet
