import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { filterElement } from '../../utils/filter'

import { EditLink, AvailableLink, LockedLink, NestedLink, ExportLink } from '../common/ElementLinks'

const Question = ({ config, question, elementActions, display='list', filter=null, indent=0 }) => {

  const verboseName = gettext('question')
  const showElement = filterElement(filter, question)

  const fetchEdit = () => elementActions.fetchElement('questions', question.id)
  const toggleLocked = () => elementActions.storeElement('questions', {...question, locked: !question.locked })

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <EditLink element={question} verboseName={verboseName} onClick={fetchEdit} />
        <LockedLink element={question} verboseName={verboseName} onClick={toggleLocked} />
        <ExportLink element={question} verboseName={verboseName} />
      </div>
      <div>
        <p>
          <strong className={question.is_optional ? 'text-muted' : ''}>{gettext('Question')}{': '}</strong>
          {question.text}
        </p>
        <p>
          <code className="code-questions">{question.uri}</code>
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
      return showElement && (
        <div className="panel panel-default panel-nested" style={{ marginLeft: 15 * indent }}>
          <div className="panel-body">
            { elementNode }
          </div>
        </div>
      )
  }
}

Question.propTypes = {
  config: PropTypes.object.isRequired,
  question: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  display: PropTypes.string,
  filter: PropTypes.object,
  indent: PropTypes.number
}

export default Question
