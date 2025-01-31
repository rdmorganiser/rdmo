import React, { useCallback } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { useDropzone } from 'react-dropzone'

const FileInput = ({ question, value, disabled, updateValue, buttons }) => {
  const onDrop = useCallback(acceptedFiles => {
    if (acceptedFiles.length == 1) {
      updateValue(value, { file: acceptedFiles[0], unit: question.unit, value_type: question.value_type })
    }
  }, [value.file])
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, disabled })

  const classnames = classNames({
    'dropzone': true,
    'disabled': disabled
  })

  return (
    <div className="interview-input file-input">
      <div className="buttons-wrapper">
        {buttons}
        <div className="file-control">
          {
            value.file_name ? (
              <div>
                <span>{gettext('Current file: ')}</span>
                <a href={value.file_url} onClick={(event) => event.stopPropagation()}>
                  {value.file_name}
                </a>
              </div>
            ) : (
              <div>{gettext('No file stored.')}</div>
            )
          }

          <div {...getRootProps({className: classnames})}>
            <input {...getInputProps()} />
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
  disabled: PropTypes.bool,
  updateValue: PropTypes.func.isRequired,
  buttons: PropTypes.node.isRequired
}

export default FileInput
