import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

import { Dropzone } from 'rdmo/core/assets/js/components'

import { getQuestionHelpId, getQuestionTextId } from '../../../../../utils/question'

const FileInput = ({ question, value, currentSet, buttons, disabled, onChange }) => {
  const handleDrop = (file) => {
    onChange(value, { file, unit: question.unit, value_type: question.value_type })
  }

  const inputProps = {
    'aria-labelledby': getQuestionTextId(question, currentSet),
    'aria-describedby': getQuestionHelpId(question, currentSet)
  }

  return (
    <div className="project-interview-input file-input">
      <div className="buttons-wrapper">
        {buttons}
        <div className="file-control">
          {
            value.file_name ? (
              <div className="mb-1">
                <span className={classNames('me-1', {'text-muted': disabled})}>{gettext('Current file:')}</span>
                <a href={value.file_url} onClick={(event) => event.stopPropagation()}>
                  {value.file_name}
                </a>
              </div>
            ) : (
              <div className="mb-1">
                {gettext('No file stored.')}
              </div>
            )
          }

          <Dropzone
            disabled={disabled}
            inputProps={inputProps}
            onDrop={handleDrop}
          />
        </div>
      </div>
    </div>
  )
}

FileInput.propTypes = {
  question: PropTypes.object.isRequired,
  value: PropTypes.object.isRequired,
  currentSet: PropTypes.object.isRequired,
  buttons: PropTypes.node.isRequired,
  disabled: PropTypes.bool.isRequired,
  onChange: PropTypes.func.isRequired,
}

export default FileInput
