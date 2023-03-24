import React, { Component } from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

import { filterElement } from '../../utils/filter'

import Question from './Question'
import { EditLink, AvailableLink, LockedLink, NestedLink, ExportLink } from '../common/ElementLinks'

const QuestionSet = ({ config, questionset, elementActions, display='list', filter=null, indent=0 }) => {

  const verboseName = gettext('question set')
  const showElement = filterElement(filter, questionset)

  const fetchEdit = () => elementActions.fetchElement('questionsets', questionset.id)
  const fetchNested = () => elementActions.fetchElement('questionsets', questionset.id, 'nested')
  const toggleLocked = () => elementActions.storeElement('questionsets', {...questionset, locked: !questionset.locked })

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <EditLink element={questionset} verboseName={verboseName} onClick={fetchEdit} />
        <LockedLink element={questionset} verboseName={verboseName} onClick={toggleLocked} />
        <NestedLink element={questionset} verboseName={verboseName} onClick={fetchNested} />
        <ExportLink element={questionset} verboseName={verboseName} />
      </div>
      <div>
        <p>
          <strong>{gettext('Question set')}{': '}</strong> {questionset.title}
        </p>
        <p>
          <code className="code-questions">{questionset.uri}</code>
        </p>
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
            showElement && <div className="panel panel-default panel-nested" style={{ marginLeft: 15 * indent }}>
              <div className="panel-heading">
                { elementNode }
              </div>
            </div>
          }
          {
            questionset.elements.map((element, index) => {
              if (isUndefined(element.text)) {
                return <QuestionSet key={index} config={config} questionset={element} elementActions={elementActions}
                                    display="nested" filter={filter}  indent={indent + 1}  />
              } else {
                return <Question key={index} config={config} question={element} elementActions={elementActions}
                                 display="nested" filter={filter}  indent={indent + 1} />
              }
            })
          }
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
