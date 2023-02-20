import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

const Questions = ({ config, questions, fetchQuestion }) => {
  const handleEdit = (event, id) => {
    event.preventDefault()
    fetchQuestion(id)
  }

  return (
    <div className="questions">
      <div className="panel panel-default">
        <div className="panel-heading">
          <div className="pull-right">
            <button className="btn btn-xs btn-default" onClick={event => history.back()}>
              {gettext('Back')}
            </button>
          </div>
          <div>
            <strong>{gettext('Questions')}</strong>
          </div>
        </div>
      </div>
      {
        filterElements(config, questions).map((question, index) => {
          return (
            <div key={index} className="panel panel-default">
              <div className="panel-heading">
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
                  <strong className={question.is_optional ? 'text-muted' : ''}>{gettext('Question')}</strong>
                  {' '}
                  <span>{question.text}</span>
                </div>
              </div>
              <div className="panel-body">
                <div><code className="code-questions" title={gettext('URI')}>{question.uri}</code></div>
                <div><code className="code-domain" title={gettext('Attribute')}>{question.attribute}</code></div>
                {
                  question.optionsets.map((optionset, index) => (
                    <div key={index}>
                      <code className="code-options" title={gettext('Option set')}>{optionset}</code>
                    </div>
                  ))
                }
              </div>
            </div>
          )
        })
      }
    </div>
  )
}

Questions.propTypes = {
  config: PropTypes.object.isRequired,
  questions: PropTypes.array.isRequired,
  fetchQuestion: PropTypes.func.isRequired
}

export default Questions
