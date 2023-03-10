import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'
import { EditLink, LockedLink, ExportLink } from '../common/ElementLinks'

const QuestionSets = ({ config, questionsets, fetchQuestionSet, storeQuestionSet }) => {
  const handleEdit = (event, id) => {
    event.preventDefault()
    fetchQuestionSet(id)
  }

  return (
    <div className="panel panel-default">
      <ElementsHeading verboseName={gettext('Catalogs')} />
      <ul className="list-group">
      {
        filterElements(config, questionsets).map((questionset, index) => {
          return (
            <li key={index} className="list-group-item">
              <div className="element-options">
                <EditLink element={questionset} verboseName={gettext('questionset')}
                          onClick={questionset => fetchQuestionSet(questionset.id)} />
                <LockedLink element={questionset} verboseName={gettext('questionset')}
                            onClick={locked => storeQuestionSet(Object.assign({}, questionset, { locked }))} />
                <ExportLink element={questionset} verboseName={gettext('questionset')} />
              </div>
              <div>
                <p>
                  <strong>{gettext('Question set')}{': '}</strong> {questionset.title}
                </p>
                <p>
                  <code className="code-questions">{questionset.uri}</code>
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

QuestionSets.propTypes = {
  config: PropTypes.object.isRequired,
  questionsets: PropTypes.array.isRequired,
  fetchQuestionSet: PropTypes.func.isRequired,
  storeQuestionSet: PropTypes.func.isRequired
}

export default QuestionSets
