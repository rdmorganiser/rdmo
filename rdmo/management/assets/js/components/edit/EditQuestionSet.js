import React from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap'
import get from 'lodash/get'
import isUndefined from 'lodash/isUndefined'
import orderBy from 'lodash/orderBy'

import Checkbox from './common/Checkbox'
import OrderedMultiSelect from './common/OrderedMultiSelect'
import MultiSelect from './common/MultiSelect'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'
import { ReadOnlyIcon } from '../common/Icons'

import QuestionSetInfo from '../info/QuestionSetInfo'
import DeleteQuestionSetModal from '../modals/DeleteQuestionSetModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditQuestionSet = ({ config, questionset, elements, elementActions }) => {

  const { sites } = config
  const { elementAction, parent, attributes, conditions } = elements

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
  const storeQuestionSet = (back) => elementActions.storeElement('questionsets', questionset, back)
  const deleteQuestionSet = () => elementActions.deleteElement('questionsets', questionset)

  const editElement = (value) => {
    if (value.questionset) {
      elementActions.fetchElement('questionsets', value.questionset)
    } else if (value.question) {
      elementActions.fetchElement('questions', value.question)
    }
  }
  const createQuestionSet = () => elementActions.createElement('questionsets', { questionset })
  const createQuestion = () => elementActions.createElement('questions', { questionset })

  const editCondition = (condition) => elementActions.fetchElement('conditions', condition)
  const createCondition = () => elementActions.createElement('conditions', { questionset })

  const editAttribute = (attribute) => elementActions.fetchElement('attributes', attribute)
  const createAttribute = () => elementActions.createElement('attributes', { questionset })

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <QuestionSetInfo questionset={questionset} elements={elements} elementActions={elementActions} />

  // for reasons unknown, the strings are not picked up by makemessages from the props
  const addElementText = gettext('Add existing element')
  const createQuestionText = gettext('Create new question')
  const createQuestionSetText = gettext('Create new question set')

  return (
    <div className="panel panel-default panel-edit">
      <div className="panel-heading">
        <div className="pull-right">
          <ReadOnlyIcon title={gettext('This question set is read only')} show={questionset.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeQuestionSet} disabled={questionset.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeQuestionSet} disabled={questionset.read_only} back={true}/>
        </div>
        {
          questionset.id ? <>
            <strong>{gettext('Question set')}{': '}</strong>
            <code className="code-questions">{questionset.uri}</code>
          </> : <strong>{gettext('Create question set')}</strong>
        }
      </div>

      {
        parent && parent.page && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This question set will be added to the page <code class="code-questions">%s</code>.'), [parent.page.uri])
          }} />
        </div>
      }
      {
        parent && parent.questionset && <div className="panel-body panel-border">
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
        </div>

        <Textarea config={config} element={questionset} field="comment"
                  rows={4} onChange={updateQuestionSet} />

        <div className="row">
          <div className="col-sm-6">
            <Checkbox config={config} element={questionset} field="locked"
                      onChange={updateQuestionSet} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={questionset} field="is_collection"
                      onChange={updateQuestionSet} />
          </div>
        </div>

        <Tabs id="#catalog-tabs" defaultActiveKey={0} animation={false}>
          {
            config.settings && config.settings.languages.map(([lang_code, lang], index) => (
              <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                <Text config={config} element={questionset} field={`title_${lang_code }`}
                      onChange={updateQuestionSet} />
                <Textarea config={config} element={questionset} field={`help_${lang_code }`}
                          rows={4} onChange={updateQuestionSet} />
                <Text config={config} element={questionset} field={`verbose_name_${lang_code }`}
                      onChange={updateQuestionSet} />
              </Tab>
            ))
          }
        </Tabs>

        <Select config={config} element={questionset} field="attribute" createText={gettext('Create new attribute')}
                options={attributes} onChange={updateQuestionSet} onCreate={createAttribute} onEdit={editAttribute} />

        <OrderedMultiSelect config={config} element={questionset} field="elements"
                            values={elementValues} options={elementOptions}
                            addText={addElementText} createText={createQuestionText}
                            altCreateText={createQuestionSetText}
                            onChange={updateQuestionSet} onCreate={createQuestion} onAltCreate={createQuestionSet}
                            onEdit={editElement}/>

        <MultiSelect config={config} element={questionset} field="conditions" options={conditions}
                     addText={gettext('Add existing condition')} createText={gettext('Create new condition')}
                     onChange={updateQuestionSet} onCreate={createCondition} onEdit={editCondition} />

        {get(config, 'settings.multisite') && <Select config={config} element={questionset} field="editors"
                                                      options={sites} onChange={updateQuestionSet} isMulti />}
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeQuestionSet} disabled={questionset.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeQuestionSet} disabled={questionset.read_only} back={true}/>
        </div>
        {questionset.id && <DeleteButton onClick={openDeleteModal} disabled={questionset.read_only} />}
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
