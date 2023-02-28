import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'

const Questions = ({ config, questions, fetchQuestion }) => {
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
              <div className="pull-right">
                <a href="" className="fa fa-pencil"
                   title={gettext('Edit question')}
                   onClick={event => handleEdit(event, question.id)}>
                </a>
                {' '}
                <a href={question.xml_url} className="fa fa-download"
                   title={gettext('Export question as XML')}
                   target="blank">
                </a>
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
  fetchQuestion: PropTypes.func.isRequired
}

export default Questions
