import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import { filterElement } from '../../utils/filter'
import { buildPath } from '../../utils/location'

import QuestionSet from './QuestionSet'
import Question from './Question'
import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, AddLink, LockedLink, NestedLink,
         ExportLink, CodeLink, ShowElementsLink } from '../common/Links'
import { ReadOnlyIcon } from '../common/Icons'
import { Drag, Drop } from '../common/DragAndDrop'

const Page = ({ config, page, configActions, elementActions, display='list', indent=0,
                filter=false, filterEditors=false, order }) => {

  const showElement = filterElement(config, filter, false, filterEditors, page)
  const showElements = get(config, `display.elements.pages.${page.id}`, true)

  const editUrl = buildPath(config.baseUrl, 'pages', page.id)
  const copyUrl = buildPath(config.baseUrl, 'pages', page.id, 'copy')
  const nestedUrl = buildPath(config.baseUrl, 'pages', page.id, 'nested')
  const exportUrl = buildPath(config.apiUrl, 'questions', 'pages', page.id, 'export')
  const attributeUrl = buildPath(config.apiUrl, 'domain', 'attributes', page.attribute)

  const getConditionUrl = (index) => buildPath(config.apiUrl, 'conditions', 'conditions', page.conditions[index])

  const fetchEdit = () => elementActions.fetchElement('pages', page.id)
  const fetchCopy = () => elementActions.fetchElement('pages', page.id, 'copy')
  const fetchNested = () => elementActions.fetchElement('pages', page.id, 'nested')
  const toggleLocked = () => elementActions.storeElement('pages', {...page, locked: !page.locked })
  const toggleElements = () => configActions.toggleElements(page)

  const createQuestionSet = () => elementActions.createElement('questionsets', { page })
  const createQuestion = () => elementActions.createElement('questions', { page })

  const fetchAttribute = () => elementActions.fetchElement('attributes', page.attribute)
  const fetchCondition = (index) => elementActions.fetchElement('conditions', page.conditions[index])

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <ReadOnlyIcon title={gettext('This page is read only')} show={page.read_only} />
        <NestedLink title={gettext('View page nested')} href={nestedUrl} onClick={fetchNested} show={display != 'nested'} />
        <ShowElementsLink showElements={showElements} show={display == 'nested'} onClick={toggleElements} />
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
      <div>
        <p>
          <strong>{gettext('Page')}{': '}</strong>
          <span dangerouslySetInnerHTML={{ __html: page.title }}></span>
        </p>
        {
          get(config, 'display.uri.pages', true) && <p>
            <CodeLink
              className="code-questions"
              uri={page.uri}
              href={editUrl}
              onClick={() => fetchEdit()}
              order={order}
            />
          </p>
        }
        {
          get(config, 'display.uri.attributes', true) && page.attribute_uri && <p>
            <CodeLink
              className="code-domain"
              uri={page.attribute_uri}
              href={attributeUrl}
              onClick={() => fetchAttribute()}
            />
          </p>
        }
        {
          get(config, 'display.uri.conditions', true) && page.condition_uris.map((uri, index) => (
            <p key={index}>
              <CodeLink
                className="code-conditions"
                uri={uri}
                href={getConditionUrl(index)}
                onClick={() => fetchCondition(index)}
              />
            </p>
          ))
        }
        <ElementErrors element={page} />
      </div>
    </div>
  )

  switch (display) {
    case 'list':
      return showElement && (
        <li className="list-group-item">
          { elementNode }
        </li>
      )
    case 'nested':
      return (
        <>
          {
            showElement && (
              <Drop element={page} elementActions={elementActions}>
                <div className="panel panel-default panel-nested" style={{ marginLeft: 30 * indent }}>
                  <div className="panel-heading">
                    { elementNode }
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
                return <QuestionSet key={index} config={config} questionset={element}
                                    configActions={configActions} elementActions={elementActions}
                                    display="nested" filter={filter} indent={indent + 1} order={questionSetOrder} />
              } else {
                const questionInfo = page.questions.find(info => info.question === element.id)
                const questionOrder = questionInfo ? questionInfo.order : undefined
                return <Question key={index} config={config} question={element}
                                 configActions={configActions} elementActions={elementActions}
                                 display="nested" filter={filter} indent={indent + 1} order={questionOrder} />
              }
            })
          }
          <Drop element={page} elementActions={elementActions} indent={indent} mode="after" />
        </>
      )
    case 'plain':
      return elementNode
  }
}

Page.propTypes = {
  config: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  display: PropTypes.string,
  indent: PropTypes.number,
  filter: PropTypes.string,
  filterEditors: PropTypes.bool,
  order: PropTypes.number
}

export default Page
