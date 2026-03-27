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
  AddLink, CodeLink, CopyLink, EditLink, ExportLink, LockedLink, NestedLink,
  ShowElementsLink
} from '../common/Links'

import Question from './Question'
import QuestionSet from './QuestionSet'

const Page = ({ page, display = 'list', indent = 0, filter = false, filterEditors = false, order }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const showElement = filterElement(config, filter, false, filterEditors, page)
  const showElements = isTruthy(get(config, `display.elements.pages.${page.id}`, true))

  const editUrl = buildPath('pages', page.id)
  const copyUrl = buildPath('pages', page.id, 'copy')
  const nestedUrl = buildPath('pages', page.id, 'nested')
  const exportUrl = buildApiPath('questions', 'pages', page.id, 'export')
  const attributeUrl = buildPath('attributes', page.attribute)

  const getConditionUrl = (index) => buildPath('conditions', page.conditions[index])

  const fetchEdit = () => dispatch(fetchElement('pages', page.id))
  const fetchCopy = () => dispatch(fetchElement('pages', page.id, 'copy'))
  const fetchNested = () => dispatch(fetchElement('pages', page.id, 'nested'))
  const toggleLocked = () => dispatch(storeElement('pages', { ...page, locked: !page.locked }))
  const toggleShowElements = () => dispatch(toggleElements(page))

  const createQuestionSet = () => dispatch(createElement('questionsets', { page }))
  const createQuestion = () => dispatch(createElement('questions', { page }))

  const fetchAttribute = () => dispatch(fetchElement('attributes', page.attribute))
  const fetchCondition = (index) => dispatch(fetchElement('conditions', page.conditions[index]))

  const displayUriPages = isTruthy(get(config, 'display.uri.pages', true))
  const displayUriAttributes = isTruthy(get(config, 'display.uri.attributes', true))
  const displayUriConditions = isTruthy(get(config, 'display.uri.conditions', true))

  const elementNode = (
    <div className="d-flex flex-column gap-2">
      <div className="d-flex align-items-center gap-2">
        <strong>{gettext('Page')}{':'}</strong>
        <div className="flex-grow-1">
          <Html html={page.title} />
        </div>

        <div className="d-flex align-items-center gap-1">
          <ReadOnlyIcon title={gettext('This page is read only')} show={page.read_only} />
          <NestedLink
            title={gettext('View page nested')}
            href={nestedUrl}
            onClick={fetchNested}
            show={display != 'nested'}
          />
          <ShowElementsLink showElements={showElements} show={display == 'nested'} onClick={toggleShowElements} />
          <EditLink title={gettext('Edit page')} href={editUrl} onClick={fetchEdit} />
          <CopyLink title={gettext('Copy page')} href={copyUrl} onClick={fetchCopy} />
          <AddLink title={gettext('Add question')} altTitle={gettext('Add question set')}
            onClick={createQuestion} onAltClick={createQuestionSet} disabled={page.read_only} />
          <LockedLink title={page.locked ? gettext('Unlock page') : gettext('Lock page')}
            locked={page.locked} onClick={toggleLocked} disabled={page.read_only} />
          <ExportLink title={gettext('Export page')} exportUrl={exportUrl}
            exportFormats={config.settings.export_formats} full={true} />
          <Drag element={page} show={display == 'nested'} />
        </div>
      </div>
      {
        displayUriPages && (
          <CodeLink
            type="questions"
            uri={page.uri}
            href={editUrl}
            onClick={() => fetchEdit()}
            order={order}
          />
        )
      }
      {
        displayUriAttributes && page.attribute_uri && (
          <CodeLink
            type="domain"
            uri={page.attribute_uri}
            href={attributeUrl}
            onClick={() => fetchAttribute()}
          />
        )
      }
      {
        displayUriConditions && page.condition_uris.map((uri, index) => (
          <CodeLink
            key={index}
            type="conditions"
            uri={uri}
            href={getConditionUrl(index)}
            onClick={() => fetchCondition(index)}
          />
        ))
      }
      <ElementErrors element={page} />
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
              <Drop element={page}>
                <div className="card mt-2" style={{ marginLeft: `calc(${indent} * var(--rdmo-management-indent))` }}>
                  <div className="card-body">
                    {elementNode}
                  </div>
                </div>
              </Drop>
            )
          }
          {
            showElements && page.elements.map((element, index) => {
              if (element.model == 'questions.questionset') {
                const questionSetInfo = page.questionsets.find(info => info.questionset === element.id)
                const questionSetOrder = questionSetInfo ? questionSetInfo.order : undefined
                return (
                  <QuestionSet key={index} config={config} questionset={element}
                    display="nested" filter={filter} indent={indent + 1} order={questionSetOrder} />
                )
              } else {
                const questionInfo = page.questions.find(info => info.question === element.id)
                const questionOrder = questionInfo ? questionInfo.order : undefined
                return (
                  <Question key={index} config={config} question={element}
                    display="nested" filter={filter} indent={indent + 1} order={questionOrder} />
                )
              }
            })
          }
          <Drop element={page} indent={indent} mode="after" />
        </div>
      )
    case 'plain':
      return elementNode
  }
}

Page.propTypes = {
  page: PropTypes.object.isRequired,
  display: PropTypes.string,
  indent: PropTypes.number,
  filter: PropTypes.string,
  filterEditors: PropTypes.bool,
  order: PropTypes.number
}

export default Page
