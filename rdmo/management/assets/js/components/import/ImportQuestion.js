import React from 'react'
import PropTypes from 'prop-types'

import { CodeLink, WarningLink, ErrorLink, ShowLink } from '../common/Links'

import Errors from './common/Errors'
import Fields from './common/Fields'
import Form from './common/Form'
import Warnings from './common/Warnings'

import { codeClass } from '../../constants/elements'

const ImportQuestion = ({ config, question, importActions }) => {
  const showFields = () => importActions.updateElement(question, {show: !question.show})
  const toggleImport = () => importActions.updateElement(question, {import: !question.import})
  const updateQuestion = (key, value) => importActions.updateElement(question, {[key]: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <WarningLink element={question} onClick={showFields} />
        <ErrorLink element={question} onClick={showFields} />
        <ShowLink element={question} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label className="mr-5">
          <input type="checkbox" checked={question.import} onChange={toggleImport} />
          <strong>{gettext('Question')}</strong>
        </label>
        <CodeLink className={codeClass[question.model]} uri={question.uri} onClick={showFields} />
      </div>
      {
        question.show && <>
          <Form config={config} element={question} updateElement={updateQuestion} />
          <Fields element={question} />
          <Warnings element={question} />
          <Errors element={question} />
        </>
      }
    </li>
  )
}

ImportQuestion.propTypes = {
  config: PropTypes.object.isRequired,
  question: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportQuestion
