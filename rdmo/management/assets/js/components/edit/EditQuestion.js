import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap'

import Html from 'rdmo/core/assets/js/components/Html'

import { fetchElement, storeElement, createElement, deleteElement, updateElement } from '../../actions/elementActions'

import Checkbox from './common/Checkbox'
import MultiSelect from './common/MultiSelect'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'
import { ReadOnlyIcon } from '../common/Icons'

import QuestionInfo from '../info/QuestionInfo'
import DeleteQuestionModal from '../modals/DeleteQuestionModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditQuestion = ({ question }) => {
  const dispatch = useDispatch()

  const { sites, widgetTypes, valueTypes, settings } = useSelector((state) => state.config)
  const { elementAction, parent, attributes, optionsets, options, conditions } = useSelector((state) => state.elements)

  const updateQuestion = (key, value) => dispatch(updateElement(question, {[key]: value}))
  const storeQuestion = (back) => dispatch(storeElement('questions', question, elementAction, back))
  const deleteQuestion = () => dispatch(deleteElement('questions', question))

  const editOptionSet = (optionset) => dispatch(fetchElement('optionsets', optionset))
  const createOptionSet = () => dispatch(createElement('optionsets', { question }))

  const editCondition = (condition) => dispatch(fetchElement('conditions', condition))
  const createCondition = () => dispatch(createElement('conditions', { question }))

  const editAttribute = (attribute) => dispatch(fetchElement('attributes', attribute))
  const createAttribute = () => dispatch(createElement('attributes', { question }))

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <QuestionInfo question={question} />

  // for reasons unknown, the strings are not picked up by makemessages from the props
  const addOptionText = gettext('Add existing optionset')
  const createOptionText = gettext('Create new optionset')

  return (
    <div className="panel panel-default panel-edit">
      <div className="panel-heading">
        <div className="pull-right">
          <ReadOnlyIcon title={gettext('This question is read only')} show={question.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeQuestion} disabled={question.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeQuestion} disabled={question.read_only} back={true}/>
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
        <Html html={interpolate(gettext(
          'This question will be added to the page <code class="code-questions">%s</code>.'),
          [parent.page.uri])} />
        </div>
      }
      {
        parent && parent.questionset && <div className="panel-body panel-border">
        <Html html={interpolate(gettext(
          'This question will be added to the question set <code class="code-questions">%s</code>.'),
          [parent.questionset.uri])} />
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
            <UriPrefix element={question} field="uri_prefix" onChange={updateQuestion} />
          </div>
          <div className="col-sm-6">
            <Text element={question} field="uri_path" onChange={updateQuestion} />
          </div>
        </div>

        <Textarea element={question} field="comment" rows={4} onChange={updateQuestion} />

        <div className="row">
          <div className="col-sm-4">
            <Checkbox element={question} field="locked" onChange={updateQuestion} />
          </div>
          <div className="col-sm-4">
            <Checkbox element={question} field="is_collection" onChange={updateQuestion} />
          </div>
          <div className="col-sm-4">
            <Checkbox element={question} field="is_optional" onChange={updateQuestion} />
          </div>
        </div>

        <Tabs id="#question-tabs" defaultActiveKey={0} animation={false}>
          {
            settings.languages.map(([lang_code, lang], index) => (
              <Tab key={index} eventKey={index} title={lang}>
                <Text element={question} field={`text_${lang_code }`} onChange={updateQuestion} />
                <Textarea element={question} field={`help_${lang_code }`} rows={8} onChange={updateQuestion} />
                <Text element={question} field={`verbose_name_${lang_code }`} onChange={updateQuestion} />
              </Tab>
            ))
          }
        </Tabs>

        <Select element={question} field="attribute" createText={gettext('Create new attribute')}
                options={attributes} onChange={updateQuestion} onCreate={createAttribute} onEdit={editAttribute} />

        <div className="row">
          <div className="col-sm-3">
            <Select element={question} field="widget_type" options={widgetTypes} onChange={updateQuestion} />
          </div>
          <div className="col-sm-3">
            <Select element={question} field="value_type" options={valueTypes} onChange={updateQuestion} />
          </div>
          <div className="col-sm-3">
            <Text element={question} field="unit" onChange={updateQuestion} />
          </div>
          <div className="col-sm-3">
            <Text element={question} field="width" onChange={updateQuestion} />
          </div>
        </div>

        <Tabs id="#question-tabs2" defaultActiveKey={0} animation={false}>
          <Tab key={0} eventKey={0} title={gettext('Conditions')}>
            <MultiSelect element={question} field="conditions" options={conditions}
                         addText={gettext('Add existing condition')} createText={gettext('Create new condition')}
                         onChange={updateQuestion} onCreate={createCondition} onEdit={editCondition} />
          </Tab>
          <Tab key={1} eventKey={1} title={gettext('Option sets')}>
            <MultiSelect element={question} field="optionsets" options={optionsets}
                         addText={addOptionText} createText={createOptionText}
                         onChange={updateQuestion} onCreate={createOptionSet} onEdit={editOptionSet} />
          </Tab>
          <Tab key={2} eventKey={2} title={gettext('Range')}>
            <div className="row">
              <div className="col-sm-4">
                <Text element={question} field="minimum" onChange={updateQuestion} />
              </div>
              <div className="col-sm-4">
                <Text element={question} field="maximum" onChange={updateQuestion} />
              </div>
              <div className="col-sm-4">
                <Text element={question} field="step" onChange={updateQuestion} />
              </div>
            </div>
          </Tab>
          <Tab key={3} eventKey={3} title={gettext('Default')}>
            {
              settings.languages.map((language, index) => (
                <Textarea key={index} element={question} field={`default_text_${language[0]}`}
                          rows={1} onChange={updateQuestion} />
              ))
            }
            <div className="row">
              <div className="col-sm-6">
                <Select element={question} field="default_option" options={options} onChange={updateQuestion} />
              </div>
              <div className="col-sm-6">
                <Text element={question} field="default_external_id" onChange={updateQuestion} />
              </div>
            </div>
          </Tab>
          {
            settings.multisite && (
              <Tab key={4} eventKey={4} title={gettext('Editors')}>
                <Select element={question} field="editors" options={sites} onChange={updateQuestion} isMulti />
              </Tab>
            )
          }
        </Tabs>
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeQuestion} disabled={question.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeQuestion} disabled={question.read_only} back={true}/>
        </div>
        {question.id && <DeleteButton onClick={openDeleteModal} disabled={question.read_only} />}
      </div>

      <DeleteQuestionModal question={question} info={info} show={showDeleteModal}
                           onClose={closeDeleteModal} onDelete={deleteQuestion} />
    </div>
  )
}

EditQuestion.propTypes = {
  question: PropTypes.object.isRequired
}

export default EditQuestion
