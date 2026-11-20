import React,  { useState } from 'react'
import PropTypes from 'prop-types'
import { useDropzone } from 'react-dropzone'
import classNames from 'classnames'

const Dropzone = ({ label, activeLabel, acceptedTypes, disabled = false, inputProps = {}, onDrop }) => {
  const [errorMessage, setErrorMessage] = useState('')

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: acceptedTypes,
    disabled,
    onDropAccepted: acceptedFiles => {
      if (acceptedFiles.length > 0) {
        onDrop(acceptedFiles[0])
        setErrorMessage('')
      }
    },
    onDropRejected: rejectedFiles => {
      setErrorMessage(interpolate(gettext('%s has unsupported file type'), [rejectedFiles[0].path]))
    }
  })

  return (
    <div {...getRootProps({className: classNames('dropzone', {'drag-active': isDragActive, disabled})})} >
      <input {...getInputProps(inputProps)} />
      {
        isDragActive ? (
          <div>
            {activeLabel || gettext('Drop the file here ...')}
          </div>
        ) : (
          <div>
            {label || gettext('Drag and drop a file here or click to select a file')}
          </div>
        )
      }
      {errorMessage && <div className="alert alert-danger mt-2">{errorMessage}</div>}
    </div>
  )
}

Dropzone.propTypes = {
  label: PropTypes.oneOfType([PropTypes.node, PropTypes.string]),
  activeLabel: PropTypes.oneOfType([PropTypes.node, PropTypes.string]),
  acceptedTypes: PropTypes.object,
  disabled: PropTypes.bool,
  inputProps: PropTypes.object,
  onDrop: PropTypes.func.isRequired,
}

export default Dropzone
