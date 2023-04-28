import React, { Component } from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

import { CodeLink, ShowLink } from '../common/Links'

import Fields from './common/Fields'
import Form from './common/Form'

import { codeClass } from '../../constants/elements'

const ImportQuestion = ({ config, question, importActions }) => {
  const showFields = () => importActions.updateElement(question, {show: !question.show})
  const toggleImport = () => importActions.updateElement(question, {import: !question.import})
  const updateQuestion = (key, value) => importActions.updateElement(question, {key: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <ShowLink element={question} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label className="mr-5">
          <input type="checkbox" checked={question.import} onChange={toggleImport} />
          <strong>{gettext('Question')}</strong>
        </label>
        <CodeLink className={codeClass[question.type]} uri={question.uri} onClick={showFields} />
      </div>
      {
        question.show && <>
          <Form config={config} element={question} updateElement={updateQuestion} />
          <Fields element={question} />
        </>
      }
    </li>
  )
}

ImportQuestion.propTypes = {
  question: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportQuestion