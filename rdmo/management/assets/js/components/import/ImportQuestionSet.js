import React from 'react'
import PropTypes from 'prop-types'

import { CodeLink, WarningLink, ErrorLink, ShowLink } from '../common/Links'

import Errors from './common/Errors'
import Fields from './common/Fields'
import Form from './common/Form'
import Warnings from './common/Warnings'

import { codeClass } from '../../constants/elements'

const ImportQuestionSet = ({ config, questionset, importActions }) => {
  const showFields = () => importActions.updateElement(questionset, {show: !questionset.show})
  const toggleImport = () => importActions.updateElement(questionset, {import: !questionset.import})
  const updateQuestionSet = (key, value) => importActions.updateElement(questionset, {[key]: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <WarningLink element={questionset} onClick={showFields} />
        <ErrorLink element={questionset} onClick={showFields} />
        <ShowLink element={questionset} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label className="mr-5">
          <input type="checkbox" checked={questionset.import} onChange={toggleImport} />
          <strong>{gettext('Question set')}</strong>
        </label>
        <CodeLink className={codeClass[questionset.model]} uri={questionset.uri} onClick={showFields} />
      </div>
      {
        questionset.show && <>
          <Form config={config} element={questionset} updateElement={updateQuestionSet} />
          <Fields element={questionset} />
          <Warnings element={questionset} />
          <Errors element={questionset} />
        </>
      }
    </li>
  )
}

ImportQuestionSet.propTypes = {
  config: PropTypes.object.isRequired,
  questionset: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportQuestionSet
