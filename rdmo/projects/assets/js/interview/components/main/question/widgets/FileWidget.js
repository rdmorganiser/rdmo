import React, { useCallback } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { useDropzone } from 'react-dropzone'

import AddValue from './common/AddValue'
import RemoveValue from './common/RemoveValue'

const FileInput = ({ value, disabled, updateValue }) => {
  const onDrop = useCallback(acceptedFiles => {
    if (acceptedFiles.length == 1) {
      updateValue(value, { file: acceptedFiles[0] })
    }
  }, [])
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, disabled })

  const classnames = classNames({
    'dropzone': true,
    'disabled': disabled
  })

  return (
    <div className="file-control">
      <div {...getRootProps({className: classnames})}>
        <input {...getInputProps()} />
        <p className="text-muted">
          {
            isDragActive ? (
              <span>{gettext('Drop the files here ...')}</span>
            ) : (
              <span>{gettext('Drag \'n drop some files here, or click to select files.')}</span>
            )
          }
        </p>
        <p>
          <span>{gettext('Current file: ')}</span>
          <a href={value.file_url} onClick={(event) => event.stopPropagation()}>
            {value.file_name}
          </a>
        </p>
      </div>
    </div>
  )
}

FileInput.propTypes = {
  value: PropTypes.object.isRequired,
  disabled: PropTypes.bool,
  updateValue: PropTypes.func.isRequired
}

const FileWidget = ({ question, values, currentSet, disabled, createValue, updateValue, deleteValue }) => {
  return (
    <div className="interview-collection">
      {
        values.map((value, valueIndex) => (
          <div key={valueIndex} className="interview-input">
            <div className="interview-input-options">
              {
                question.is_collection && <RemoveValue value={value} deleteValue={deleteValue} />
              }
            </div>
            <FileInput
              value={value}
              disabled={disabled}
              updateValue={updateValue}
            />
          </div>
        ))
      }
      {
        question.is_collection && (
          <AddValue question={question} values={values} currentSet={currentSet} createValue={createValue} />
        )
      }
    </div>
  )
}

FileWidget.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  disabled: PropTypes.bool,
  currentSet: PropTypes.object.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired
}

export default FileWidget
