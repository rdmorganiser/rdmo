import React, { Component } from 'react'
import PropTypes from 'prop-types'
import uniqueId from 'lodash/uniqueId'

import { ShowLink } from '../common/Links'

import Fields from './common/Fields'
import Form from './common/Form'

import { codeClass } from '../../constants/elements'

const ImportQuestionSet = ({ config, questionset, importActions }) => {
  const showFields = () => importActions.updateElement(questionset, {show: !questionset.show})
  const toggleImport = () => importActions.updateElement(questionset, {import: !questionset.import})
  const updateQuestionSet = (key, value) => importActions.updateElement(questionset, {key: value})

  return (
    <li className="list-group-item">
      <div className="pull-right">
        <ShowLink element={questionset} onClick={showFields} />
      </div>
      <div className="checkbox">
        <label>
          <input type="checkbox" checked={questionset.import} onChange={toggleImport} />
          <strong>{gettext('Question set')}{' '}</strong>
          <code className={codeClass[questionset.type]}>{questionset.uri}</code>
        </label>
      </div>
      {
        questionset.show && <>
          <Form config={config} element={questionset} updateElement={updateQuestionSet} />
          <Fields element={questionset} />
        </>
      }
    </li>
  )
}

ImportQuestionSet.propTypes = {
  questionset: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

export default ImportQuestionSet