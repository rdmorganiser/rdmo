import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'
import { EditLink, LockedLink, ExportLink } from '../common/ElementLinks'

const Questions = ({ config, questions, fetchQuestion, storeQuestion }) => {
  const handleEdit = (event, id) => {
    event.preventDefault()
    fetchQuestion(id)
  }

  return (
    <div className="panel panel-default">
      <ElementsHeading verboseName={gettext('Catalogs')} />
      <ul className="list-group">
      {
        filterElements(config, questions).map((question, index) => {
          return (
            <li key={index} className="list-group-item">
              <div className="element-options">
                <EditLink element={question} verboseName={gettext('question')}
                          onClick={question => fetchQuestion(question.id)} />
                <LockedLink element={question} verboseName={gettext('question')}
                            onClick={locked => storeQuestion(Object.assign({}, question, { locked }))} />
                <ExportLink element={question} verboseName={gettext('question')} />
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
            </li>
          )
        })
      }
      </ul>
    </div>
  )
}

Questions.propTypes = {
  config: PropTypes.object.isRequired,
  questions: PropTypes.array.isRequired,
  fetchQuestion: PropTypes.func.isRequired,
  storeQuestion: PropTypes.func.isRequired
}

export default Questions
