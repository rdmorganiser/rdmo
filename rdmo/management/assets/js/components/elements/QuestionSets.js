import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'

const QuestionSets = ({ config, questionsets, fetchQuestionSet }) => {
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
              <div className="pull-right">
                <a href="" className="fa fa-pencil"
                   title={gettext('Edit questionset')}
                   onClick={event => handleEdit(event, questionset.id)}>
                </a>
                {' '}
                <a href={questionset.xml_url} className="fa fa-download"
                   title={gettext('Export questionset as XML')}
                   target="blank">
                </a>
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
  fetchQuestionSet: PropTypes.func.isRequired
}

export default QuestionSets
