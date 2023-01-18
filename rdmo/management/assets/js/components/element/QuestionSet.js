import React from 'react'
import PropTypes from 'prop-types'

import { filterElement } from '../../utils/filter'

import Question from './Question'
import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, AddLink, LockedLink,
         NestedLink, ExportLink, CodeLink } from '../common/Links'
import { Drag, Drop } from '../common/DragAndDrop'

const QuestionSet = ({ config, questionset, elementActions, display='list', filter=null, indent=0 }) => {

  const verboseName = gettext('question set')
  const showElement = filterElement(filter, questionset)

  const fetchEdit = () => elementActions.fetchElement('questionsets', questionset.id)
  const fetchCopy = () => elementActions.fetchElement('questionsets', questionset.id, 'copy')
  const fetchNested = () => elementActions.fetchElement('questionsets', questionset.id, 'nested')
  const toggleLocked = () => elementActions.storeElement('questionsets', {...questionset, locked: !questionset.locked })

  const createQuestionSet = () => elementActions.createElement('questionsets', { questionset })
  const createQuestion = () => elementActions.createElement('questions', { questionset })

  const fetchAttribute = () => elementActions.fetchElement('attributes', questionset.attribute)
  const fetchCondition = (index) => elementActions.fetchElement('conditions', questionset.conditions[index])

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <NestedLink element={questionset} verboseName={verboseName} onClick={fetchNested} />
        <EditLink verboseName={verboseName} onClick={fetchEdit} />
        <CopyLink verboseName={verboseName} onClick={fetchCopy} />
        <AddLink element={questionset} verboseName={gettext('question')} verboseNameAlt={gettext('question set')}
                 onClick={createQuestion} onAltClick={createQuestionSet} />
        <LockedLink element={questionset} verboseName={verboseName} onClick={toggleLocked} />
        <ExportLink element={questionset} elementType="questionsets" verboseName={verboseName}
                    exportFormats={config.settings.export_formats} />
        {display == 'nested' && <Drag element={questionset} />}
      </div>
      <div>
        <p>
          <strong>{gettext('Question set')}{': '}</strong> {questionset.title}
        </p>
        {
          config.display.uri.questionsets && <p>
            <CodeLink className="code-questions" uri={questionset.uri} onClick={() => fetchEdit()} />
          </p>
        }
        {
          config.display.uri.attributes && questionset.attribute_uri &&<p>
            <CodeLink className="code-domain" uri={questionset.attribute_uri} onClick={() => fetchAttribute()} />
          </p>
        }
        {
          config.display.uri.conditions && questionset.condition_uris.map((uri, index) => (
            <p key={index}>
              <CodeLink className="code-conditions" uri={uri} onClick={() => fetchCondition(index)} />
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
            showElement && config.display.elements.questionsets && (
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
            questionset.elements.map((element, index) => {
              if (element.model == 'questions.questionset') {
                return <QuestionSet key={index} config={config} questionset={element} elementActions={elementActions}
                                    display="nested" filter={filter}  indent={indent + 1}  />
              } else {
                return <Question key={index} config={config} question={element} elementActions={elementActions}
                                 display="nested" filter={filter}  indent={indent + 1} />
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
  elementActions: PropTypes.object.isRequired,
  display: PropTypes.string,
  filter: PropTypes.object,
  indent: PropTypes.number
}

export default QuestionSet