import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { EditLink, AvailableLink, LockedLink, NestedLink, ExportLink } from '../common/ElementLinks'

const Question = ({ config, question,elementActions, indent=0 }) => {

  const verboseName = gettext('question')

  const fetchEdit = () => elementActions.fetchElement('questions', question.id)
  const toggleLocked = () => elementActions.storeElement('questions', {...question, locked: !question.locked })

  return (
    <li className="list-group-item">
      <div className="element">
        <div className="pull-right">
          <EditLink element={question} verboseName={verboseName} onClick={fetchEdit} />
          <LockedLink element={question} verboseName={verboseName} onClick={toggleLocked} />
          <ExportLink element={question} verboseName={verboseName} />
        </div>
        <div style={{ paddingLeft: 15 * indent }}>
          <p>
            <strong className={question.is_optional ? 'text-muted' : ''}>{gettext('Question')}{': '}</strong>
            {question.text}
          </p>
          <p>
            <code className="code-questions">{question.uri}</code>
          </p>
        </div>
      </div>
    </li>
  )
}

Question.propTypes = {
  config: PropTypes.object.isRequired,
  question: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  indent: PropTypes.number
}

export default Question
