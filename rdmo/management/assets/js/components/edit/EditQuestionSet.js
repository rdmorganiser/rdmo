import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import { isUndefined, orderBy } from 'lodash'

import Html from 'rdmo/core/assets/js/components/Html'

import { fetchElement, storeElement, createElement, deleteElement, updateElement } from '../../actions/elementActions'

import Checkbox from './common/Checkbox'
import LanguageTabs from './common/LanguageTabs'
import MultiSelect from './common/MultiSelect'
import OrderedMultiSelect from './common/OrderedMultiSelect'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'
import { ReadOnlyIcon } from '../common/Icons'

import QuestionSetInfo from '../info/QuestionSetInfo'
import DeleteQuestionSetModal from '../modals/DeleteQuestionSetModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditQuestionSet = ({ questionset }) => {
  const dispatch = useDispatch()

  const { sites, settings } = useSelector((state) => state.config)
  const { elementAction, parent, attributes,
          conditions, questions, questionsets } = useSelector((state) => state.elements)

  const elementValues = orderBy(questionset.questions.concat(questionset.questionsets), ['order', 'uri'])
  const elementOptions = questions.map(question => ({
    value: 'question-' + question.id,
    label: interpolate(gettext('Question: %s'), [question.uri])
  })).concat(questionsets.map(questionset => ({
    value: 'questionset-' + questionset.id,
    label: interpolate(gettext('Question set: %s'), [questionset.uri])
  })))

  const updateQuestionSet = (key, value) => {
    if (key == 'elements') {
      dispatch(updateElement(questionset, {
        questions: value.filter(e => !isUndefined(e.question)),
        questionsets: value.filter(e => !isUndefined(e.questionset))
      }))
    } else {
      dispatch(updateElement(questionset, { [key]: value }))
    }
  }
  const storeQuestionSet = (back) => dispatch(storeElement('questionsets', questionset, elementAction, back))
  const deleteQuestionSet = () => dispatch(deleteElement('questionsets', questionset))

  const editElement = (value) => {
    if (value.questionset) {
      dispatch(fetchElement('questionsets', value.questionset))
    } else if (value.question) {
      dispatch(fetchElement('questions', value.question))
    }
  }
  const createQuestionSet = () => dispatch(createElement('questionsets', { questionset }))
  const createQuestion = () => dispatch(createElement('questions', { questionset }))

  const editCondition = (condition) => dispatch(fetchElement('conditions', condition))
  const createCondition = () => dispatch(createElement('conditions', { questionset }))

  const editAttribute = (attribute) => dispatch(fetchElement('attributes', attribute))
  const createAttribute = () => dispatch(createElement('attributes', { questionset }))

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <QuestionSetInfo questionset={questionset} />

  // for reasons unknown, the strings are not picked up by makemessages from the props
  const addElementText = gettext('Add existing element')
  const createQuestionText = gettext('Create new question')
  const createQuestionSetText = gettext('Create new question set')

  return (
    <div className="card">
      <div className="card-header">
        <div className="d-flex flex-wrap align-items-center gap-2">
          <strong className="flex-grow-1">
            {questionset.id ? gettext('Edit questionset') : gettext('Create questionset')}
          </strong>
          <ReadOnlyIcon title={gettext('This question set is read only')} show={questionset.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeQuestionSet} disabled={questionset.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeQuestionSet} disabled={questionset.read_only} back={true}/>
        </div>
      </div>

      {
        parent && parent.page && <div className="card-body border-bottom">
        <Html html={interpolate(gettext(
          'This question set will be added to the page <code class="code-questions">%s</code>.'),
          [parent.page.uri])} />
        </div>
      }
      {
        parent && parent.questionset && <div className="card-body border-bottom">
        <Html html={interpolate(gettext(
          'This question set will be added to the question set <code class="code-questions">%s</code>.'),
          [parent.questionset.uri])} />
        </div>
      }

      {
        questionset.id && <div className="card-body border-bottom">
          { info }
        </div>
      }

      <div className="card-body pb-0">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix element={questionset} field="uri_prefix" onChange={updateQuestionSet} />
          </div>
          <div className="col-sm-6">
            <Text element={questionset} field="uri_path" onChange={updateQuestionSet} />
          </div>
        </div>

        <Textarea element={questionset} field="comment" rows={4} onChange={updateQuestionSet} />

        <div className="row">
          <div className="col-sm-6">
            <Checkbox element={questionset} field="locked" onChange={updateQuestionSet} />
          </div>
          <div className="col-sm-6">
            <Checkbox element={questionset} field="is_collection" onChange={updateQuestionSet} />
          </div>
        </div>

        <LanguageTabs render={(langCode) => (
          <>
            <Text element={questionset} field={`title_${langCode}`} onChange={updateQuestionSet} />
            <Textarea element={questionset} field={`help_${langCode}`} rows={4} onChange={updateQuestionSet} />
            <Text element={questionset} field={`verbose_name_${langCode}`} onChange={updateQuestionSet} />
          </>
        )} />

        <Select element={questionset} field="attribute" createText={gettext('Create new attribute')}
                options={attributes} onChange={updateQuestionSet} onCreate={createAttribute} onEdit={editAttribute} />

        <OrderedMultiSelect element={questionset} field="elements"
                            values={elementValues} options={elementOptions}
                            addText={addElementText} createText={createQuestionText}
                            altCreateText={createQuestionSetText}
                            onChange={updateQuestionSet} onCreate={createQuestion} onAltCreate={createQuestionSet}
                            onEdit={editElement}/>

        <MultiSelect element={questionset} field="conditions" options={conditions}
                     addText={gettext('Add existing condition')} createText={gettext('Create new condition')}
                     onChange={updateQuestionSet} onCreate={createCondition} onEdit={editCondition} />

        {
          settings.multisite && (
            <Select element={questionset} field="editors" options={sites} onChange={updateQuestionSet} isMulti />
            )
        }
      </div>

      <div className="card-footer">
        <div className="d-flex align-items-center gap-2">
          {questionset.id && <DeleteButton onClick={openDeleteModal} disabled={questionset.read_only} />}
          <BackButton className="ms-auto" />
          <SaveButton elementAction={elementAction} onClick={storeQuestionSet} disabled={questionset.read_only} />
          <SaveButton elementAction={elementAction} onClick={storeQuestionSet} disabled={questionset.read_only} back={true}/>
        </div>
      </div>

      <DeleteQuestionSetModal questionset={questionset} info={info} show={showDeleteModal}
                              onClose={closeDeleteModal} onDelete={deleteQuestionSet} />
    </div>
  )
}

EditQuestionSet.propTypes = {
  questionset: PropTypes.object.isRequired
}

export default EditQuestionSet
