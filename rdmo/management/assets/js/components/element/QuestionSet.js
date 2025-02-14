import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import { filterElement } from '../../utils/filter'
import { buildApiPath, buildPath } from '../../utils/location'

import Question from './Question'
import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, AddLink, LockedLink,
         NestedLink, ExportLink, CodeLink, ShowElementsLink } from '../common/Links'
import { ReadOnlyIcon } from '../common/Icons'
import { Drag, Drop } from '../common/DragAndDrop'

const QuestionSet = ({ config, questionset, configActions, elementActions, display='list', indent=0,
                       filter=false, filterEditors=false, order }) => {

  const showElement = filterElement(config, filter, false, filterEditors, questionset)
  const showElements = get(config, `display.elements.questionsets.${questionset.id}`, true)

  const editUrl = buildPath('questionsets', questionset.id)
  const copyUrl = buildPath('questionsets', questionset.id, 'copy')
  const nestedUrl = buildPath('questionsets', questionset.id, 'nested')
  const exportUrl = buildApiPath('questions', 'questionsets', questionset.id, 'export')
  const attributeUrl = buildPath('attributes', questionset.attribute)

  const getConditionUrl = (index) => buildPath('conditions', questionset.conditions[index])

  const fetchEdit = () => elementActions.fetchElement('questionsets', questionset.id)
  const fetchCopy = () => elementActions.fetchElement('questionsets', questionset.id, 'copy')
  const fetchNested = () => elementActions.fetchElement('questionsets', questionset.id, 'nested')
  const toggleLocked = () => elementActions.storeElement('questionsets', {...questionset, locked: !questionset.locked })
  const toggleElements = () => elementActions.toggleElements(questionset)

  const createQuestionSet = () => elementActions.createElement('questionsets', { questionset })
  const createQuestion = () => elementActions.createElement('questions', { questionset })

  const fetchAttribute = () => elementActions.fetchElement('attributes', questionset.attribute)
  const fetchCondition = (index) => elementActions.fetchElement('conditions', questionset.conditions[index])

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <ReadOnlyIcon title={gettext('This question set is read only')} show={questionset.read_only} />
        <NestedLink title={gettext('View question set nested')} href={nestedUrl} onClick={fetchNested} show={display != 'nested'} />
        <ShowElementsLink showElements={showElements} show={display == 'nested'} onClick={toggleElements} />
        <EditLink title={gettext('Edit question set')} href={editUrl} onClick={fetchEdit} />
        <CopyLink title={gettext('Copy question set')} href={copyUrl} onClick={fetchCopy} />
        <AddLink title={gettext('Add question')} altTitle={gettext('Add question set')}
                 onClick={createQuestion} onAltClick={createQuestionSet} disabled={questionset.read_only} />
        <LockedLink title={questionset.locked ? gettext('Unlock question set') : gettext('Lock question set')}
                    locked={questionset.locked} onClick={toggleLocked} disabled={questionset.read_only} />
        <ExportLink title={gettext('Export question set')} exportUrl={exportUrl}
                    exportFormats={config.settings.export_formats} full={true} />
        <Drag element={questionset} show={display == 'nested'} />
      </div>
      <div>
        <p>
          <strong>{gettext('Question set')}{': '}</strong>
          <span dangerouslySetInnerHTML={{ __html: questionset.title }}></span>
        </p>
        {
          get(config, 'display.uri.questionsets', true) && <p>
            <CodeLink
              className="code-questions"
              uri={questionset.uri}
              href={editUrl}
              onClick={() => fetchEdit()}
              order={order}
            />
          </p>
        }
        {
          get(config, 'display.uri.attributes', true) && questionset.attribute_uri &&<p>
            <CodeLink
              className="code-domain"
              uri={questionset.attribute_uri}
              href={attributeUrl}
              onClick={() => fetchAttribute()}
            />
          </p>
        }
        {
          get(config, 'display.uri.conditions', true) && questionset.condition_uris.map((uri, index) => (
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
        <ElementErrors element={questionset} />
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
              <Drop element={questionset} elementActions={elementActions}>
                <div className="panel panel-default panel-nested" style={{ marginLeft: 30 * indent }}>
                  <div className="panel-heading">
                    { elementNode }
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
                return <QuestionSet key={index} config={config} questionset={element}
                                    configActions={configActions} elementActions={elementActions}
                                    display="nested" filter={filter} indent={indent + 1} order={questionSetOrder}  />
              } else {
                const questionInfo = questionset.questions.find(info => info.question === element.id)
                const questionOrder = questionInfo ? questionInfo.order : undefined
                return <Question key={index} config={config} question={element}
                                 configActions={configActions} elementActions={elementActions}
                                 display="nested" filter={filter} indent={indent + 1} order={questionOrder} />
              }
            })
          }
          <Drop element={questionset} elementActions={elementActions} indent={indent} mode="after" />
        </>
      )
    case 'plain':
      return elementNode
  }
}

QuestionSet.propTypes = {
  config: PropTypes.object.isRequired,
  questionset: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  display: PropTypes.string,
  indent: PropTypes.number,
  filter: PropTypes.string,
  filterEditors: PropTypes.bool,
  order: PropTypes.number
}

export default QuestionSet
