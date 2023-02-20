import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

const QuestionSets = ({ config, questionsets, fetchQuestionSet }) => {
  const handleEdit = (event, id) => {
    event.preventDefault()
    fetchQuestionSet(id)
  }

  return (
    <div className="questionsets">
      <div className="panel panel-default">
        <div className="panel-heading">
          <div className="pull-right">
            <button className="btn btn-xs btn-default" onClick={event => history.back()}>
              {gettext('Back')}
            </button>
          </div>
          <div>
            <strong>{gettext('Question sets')}</strong>
          </div>
        </div>
      </div>
      {
        filterElements(config, questionsets).map((questionset, index) => {
          return (
            <div key={index} className="panel panel-default">
              <div className="panel-heading">
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
                  <strong>{gettext('Question set')}:</strong>
                  {' '}
                  <span>{questionset.title}</span>
                </div>
              </div>
              <div className="panel-body">
                <strong>{gettext('URI')}:</strong>
                {' '}
                <code className="code-questions">{questionset.uri}</code>
              </div>
            </div>
          )
        })
      }
    </div>
  )
}

QuestionSets.propTypes = {
  config: PropTypes.object.isRequired,
  questionsets: PropTypes.array.isRequired,
  fetchQuestionSet: PropTypes.func.isRequired
}

export default QuestionSets
