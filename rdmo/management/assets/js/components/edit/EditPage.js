import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap'
import { isUndefined, orderBy } from 'lodash'

import Html from 'rdmo/core/assets/js/components/Html'

import { fetchElement, storeElement, createElement, deleteElement, updateElement } from '../../actions/elementActions'

import Checkbox from './common/Checkbox'
import MultiSelect from './common/MultiSelect'
import OrderedMultiSelect from './common/OrderedMultiSelect'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'
import { ReadOnlyIcon } from '../common/Icons'

import PageInfo from '../info/PageInfo'
import DeletePageModal from '../modals/DeletePageModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditPage = ({ page }) => {
  const dispatch = useDispatch()

  const { sites, settings } = useSelector((state) => state.config)
  const { elementAction, parent, attributes,
          conditions, questions, questionsets } = useSelector((state) => state.elements)

  const elementValues = orderBy(page.questions.concat(page.questionsets), ['order', 'uri'])
  const elementOptions = questions.map(question => ({
    value: 'question-' + question.id,
    label: interpolate(gettext('Question: %s'), [question.uri])
  })).concat(questionsets.map(questionset => ({
    value: 'questionset-' + questionset.id,
    label: interpolate(gettext('Question set: %s'), [questionset.uri])
  })))

  const updatePage = (key, value) => {
    if (key == 'elements') {
      dispatch(updateElement(page, {
        questions: value.filter(e => !isUndefined(e.question)),
        questionsets: value.filter(e => !isUndefined(e.questionset))
      }))
    } else {
      dispatch(updateElement(page, { [key]: value }))
    }
  }
  const storePage = (back) => dispatch(storeElement('pages', page, elementAction, back))
  const deletePage = () => dispatch(deleteElement('pages', page))

  const editElement = (value) => {
    if (value.questionset) {
      dispatch(fetchElement('questionsets', value.questionset))
    } else if (value.question) {
      dispatch(fetchElement('questions', value.question))
    }
  }
  const createQuestionSet = () => dispatch(createElement('questionsets', { page }))
  const createQuestion = () => dispatch(createElement('questions', { page }))

  const editCondition = (condition) => dispatch(fetchElement('conditions', condition))
  const createCondition = () => dispatch(createElement('conditions', { page }))

  const editAttribute = (attribute) => dispatch(fetchElement('attributes', attribute))
  const createAttribute = () => dispatch(createElement('attributes', { page }))

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <PageInfo page={page} />

  // for reasons unknown, the strings are not picked up by makemessages from the props
  const addElementText = gettext('Add existing element')
  const createQuestionText = gettext('Create new question')
  const createQuestionSetText = gettext('Create new question set')

  return (
    <div className="panel panel-default panel-edit">
      <div className="panel-heading">
        <div className="pull-right">
          <ReadOnlyIcon title={gettext('This page is read only')} show={page.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storePage} disabled={page.read_only} />
          <SaveButton elementAction={elementAction} onClick={storePage} disabled={page.read_only} back={true}/>
        </div>
        {
          page.id ? <>
            <strong>{gettext('Page')}{': '}</strong>
            <code className="code-questions">{page.uri}</code>
          </> : <strong>{gettext('Create page')}</strong>
        }
      </div>

      {
        parent && parent.section && <div className="panel-body panel-border">
        <Html html={interpolate(gettext(
          'This page will be added to the section <code class="code-questions">%s</code>.'),
          [parent.section.uri])} />
        </div>
      }

      {
        page.id && <div className="panel-body panel-border">
          { info }
        </div>
      }

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix element={page} field="uri_prefix" onChange={updatePage} />
          </div>
          <div className="col-sm-6">
            <Text element={page} field="uri_path" onChange={updatePage} />
          </div>
        </div>

        <Textarea element={page} field="comment" rows={4} onChange={updatePage} />

        <div className="row">
          <div className="col-sm-6">
            <Checkbox element={page} field="locked" onChange={updatePage} />
          </div>
          <div className="col-sm-6">
            <Checkbox element={page} field="is_collection" onChange={updatePage} />
          </div>
        </div>

        <Tabs id="#page-tabs" defaultActiveKey={0} animation={false}>
          {
            settings.languages.map(([lang_code, lang], index) => (
              <Tab key={index} eventKey={index} title={lang}>
                <Text element={page} field={`title_${lang_code }`} onChange={updatePage} />
                <Text element={page} field={`short_title_${lang_code }`} onChange={updatePage} />
                <Textarea element={page} field={`help_${lang_code }`} rows={4} onChange={updatePage} />
                <Text element={page} field={`verbose_name_${lang_code }`} onChange={updatePage} />
              </Tab>
            ))
          }
        </Tabs>



        <Select element={page} field="attribute" createText={gettext('Create new attribute')}
                options={attributes} onChange={updatePage} onCreate={createAttribute} onEdit={editAttribute} />

        <OrderedMultiSelect element={page} field="elements"
                            values={elementValues} options={elementOptions}
                            addText={addElementText} createText={createQuestionText}
                            altCreateText={createQuestionSetText}
                            onChange={updatePage} onCreate={createQuestion} onAltCreate={createQuestionSet}
                            onEdit={editElement} />

        <MultiSelect element={page} field="conditions" options={conditions}
                     addText={gettext('Add existing condition')} createText={gettext('Create new condition')}
                     onChange={updatePage} onCreate={createCondition} onEdit={editCondition} />

        {
          settings.multisite && (
            <Select element={page} field="editors" options={sites} onChange={updatePage} isMulti />
          )
        }
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storePage} disabled={page.read_only} />
          <SaveButton elementAction={elementAction} onClick={storePage} disabled={page.read_only} back={true}/>
        </div>
        {page.id && <DeleteButton onClick={openDeleteModal} disabled={page.read_only} />}
      </div>

      <DeletePageModal page={page} info={info} show={showDeleteModal}
                       onClose={closeDeleteModal} onDelete={deletePage} />
    </div>
  )
}

EditPage.propTypes = {
  page: PropTypes.object.isRequired
}

export default EditPage
