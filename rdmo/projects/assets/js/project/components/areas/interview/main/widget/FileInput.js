import React, { useCallback } from 'react'
import PropTypes from 'prop-types'
import { useDropzone } from 'react-dropzone'
import classNames from 'classnames'

import { getQuestionHelpId, getQuestionTextId } from '../../../../../utils/question'

const FileInput = ({ question, value, buttons, disabled, onChange }) => {
  const onDrop = useCallback(acceptedFiles => {
    if (acceptedFiles.length == 1) {
      onChange(value, { file: acceptedFiles[0], unit: question.unit, value_type: question.value_type })
    }
  }, [value])
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, disabled })

  const classnames = classNames('dropzone', {
    'disabled': disabled
  })

  return (
    <div className="project-interview-input file-input">
      <div className="buttons-wrapper">
        {buttons}
        <div className="file-control">
          {
            value.file_name ? (
              <div>
                <span className={classNames({'text-muted': disabled})}>{gettext('Current file:')}</span>
                <a href={value.file_url} onClick={(event) => event.stopPropagation()}>
                  {value.file_name}
                </a>
              </div>
            ) : (
              <div>{gettext('No file stored.')}</div>
            )
          }

          <div {...getRootProps({className: classnames})}>
            <input
              {...getInputProps()}
              aria-labelledby={getQuestionTextId(question)}
              aria-describedby={getQuestionHelpId(question)}
            />
            <div className="text-muted">
              {
                isDragActive ? (
                  <span>{gettext('Drop the files here ...')}</span>
                ) : (
                  <span>{gettext('Drag \'n drop some files here, or click to select files.')}</span>
                )
              }
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

FileInput.propTypes = {
  question: PropTypes.object.isRequired,
  value: PropTypes.object.isRequired,
  buttons: PropTypes.node.isRequired,
  disabled: PropTypes.bool.isRequired,
  onChange: PropTypes.func.isRequired,
}

export default FileInput
