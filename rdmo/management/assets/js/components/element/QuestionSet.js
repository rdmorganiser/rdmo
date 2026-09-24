import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import get from 'lodash/get'

import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import Html from 'rdmo/core/assets/js/components/Html'

import { createElement, fetchElement, storeElement, toggleElements } from '../../actions/elementActions'
import { filterElement } from '../../utils/filter'
import { buildApiPath, buildPath } from '../../utils/location'

import { Drag, Drop } from '../common/DragAndDrop'
import { ElementErrors } from '../common/Errors'
import { ReadOnlyIcon } from '../common/Icons'
import {
  AddLink, CodeLink, CopyLink, EditLink, ExportLink, LockedLink,
  NestedLink, ShowElementsLink
} from '../common/Links'

import Question from './Question'

const QuestionSet = ({ questionset, display = 'list', indent = 0, filter = false, filterEditors = false, order }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const showElement = filterElement(config, filter, false, filterEditors, questionset)
  const showElements = isTruthy(get(config, `display.elements.questionsets.${questionset.id}`, true))

  const editUrl = buildPath('questionsets', questionset.id)
  const copyUrl = buildPath('questionsets', questionset.id, 'copy')
  const nestedUrl = buildPath('questionsets', questionset.id, 'nested')
  const exportUrl = buildApiPath('questions', 'questionsets', questionset.id, 'export')
  const attributeUrl = buildPath('attributes', questionset.attribute)

  const getConditionUrl = (index) => buildPath('conditions', questionset.conditions[index])

  const fetchEdit = () => dispatch(fetchElement('questionsets', questionset.id))
  const fetchCopy = () => dispatch(fetchElement('questionsets', questionset.id, 'copy'))
  const fetchNested = () => dispatch(fetchElement('questionsets', questionset.id, 'nested'))
  const toggleLocked = () => dispatch(storeElement('questionsets', { ...questionset, locked: !questionset.locked }))
  const toggleShowElements = () => dispatch(toggleElements(questionset))

  const createQuestionSet = () => dispatch(createElement('questionsets', { questionset }))
  const createQuestion = () => dispatch(createElement('questions', { questionset }))

  const fetchAttribute = () => dispatch(fetchElement('attributes', questionset.attribute))
  const fetchCondition = (index) => dispatch(fetchElement('conditions', questionset.conditions[index]))

  const displayUriQuestionSets = isTruthy(get(config, 'display.uri.questionsets', true))
  const displayUriAttributes = isTruthy(get(config, 'display.uri.attributes', true))
  const displayUriConditions = isTruthy(get(config, 'display.uri.conditions', true))

  const elementNode = (
    <div className="d-flex flex-column gap-2">
      <div className="d-flex align-items-center gap-2">
        <strong>{gettext('Question set')}{':'}</strong>
        <div className="flex-grow-1">
          <Html html={questionset.title} />
        </div>

        <div className="d-flex align-items-center gap-1">
          <ReadOnlyIcon title={gettext('This question set is read only')} show={questionset.read_only} />
          <NestedLink
            title={gettext('View question set nested')}
            href={nestedUrl}
            onClick={fetchNested}
            show={display != 'nested'}
          />
          <ShowElementsLink showElements={showElements} show={display == 'nested'} onClick={toggleShowElements} />
          <EditLink title={gettext('Edit question set')} href={editUrl} onClick={fetchEdit} />
          <CopyLink title={gettext('Copy question set')} href={copyUrl} onClick={fetchCopy} />
          <AddLink
            title={gettext('Add question')} altTitle={gettext('Add question set')}
            onClick={createQuestion} onAltClick={createQuestionSet} disabled={questionset.read_only} />
          <LockedLink
            title={questionset.locked ? gettext('Unlock question set') : gettext('Lock question set')}
            locked={questionset.locked} onClick={toggleLocked} disabled={questionset.read_only} />
          <ExportLink
            title={gettext('Export question set')} exportUrl={exportUrl}
            exportFormats={config.settings.export_formats} full={true} />
          <Drag element={questionset} show={display == 'nested'} />
        </div>
      </div>
      {
        displayUriQuestionSets && (
          <span>
            <CodeLink
              type="questions"
              uri={questionset.uri}
              href={editUrl}
              onClick={() => fetchEdit()}
              order={order}
            />
          </span>
        )
      }
      {
        displayUriAttributes && questionset.attribute_uri && (
          <span>
            <CodeLink
              type="domain"
              uri={questionset.attribute_uri}
              href={attributeUrl}
              onClick={() => fetchAttribute()}
            />
          </span>
        )
      }
      {
        displayUriConditions && questionset.condition_uris.map((uri, index) => (
          <CodeLink
            key={index}
            type="conditions"
            uri={uri}
            href={getConditionUrl(index)}
            onClick={() => fetchCondition(index)}
          />
        ))
      }
      <ElementErrors element={questionset} />
    </div>
  )

  switch (display) {
    case 'list':
      return showElement && (
        <li className="list-group-item">
          {elementNode}
        </li>
      )
    case 'nested':
      return (
        <div className="position-relative">
          {
            showElement && (
              <Drop element={questionset}>
                <div className="card mt-2" style={{ marginLeft: `calc(${indent} * var(--rdmo-management-indent))` }}>
                  <div className="card-body">
                    {elementNode}
                  </div>
                </div>
              </Drop>
            )
          }
          {
            showElements && questionset.elements.map((element, index) => {
              if (element.model == 'questions.questionset') {
                const questionSetInfo = questionset.questionsets.find(info => info.questionset === element.id)
                const questionSetOrder = questionSetInfo ? questionSetInfo.order : undefined
                return (
                  <QuestionSet
                    key={index} config={config} questionset={element}
                    display="nested" filter={filter} indent={indent + 1} order={questionSetOrder} />
                )
              } else {
                const questionInfo = questionset.questions.find(info => info.question === element.id)
                const questionOrder = questionInfo ? questionInfo.order : undefined
                return (
                  <Question
                    key={index} config={config} question={element}
                    display="nested" filter={filter} indent={indent + 1} order={questionOrder} />
                )
              }
            })
          }
          <Drop element={questionset} indent={indent} mode="after" />
        </div>
      )
    case 'plain':
      return elementNode
  }
}

QuestionSet.propTypes = {
  questionset: PropTypes.object.isRequired,
  display: PropTypes.string,
  indent: PropTypes.number,
  filter: PropTypes.string,
  filterEditors: PropTypes.bool,
  order: PropTypes.number
}

export default QuestionSet
