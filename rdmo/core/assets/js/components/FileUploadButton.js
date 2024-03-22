import React from 'react'
import PropTypes from 'prop-types'
import { useDropzone } from 'react-dropzone'

const FileUploadButton = ({ acceptedTypes, buttonProps, buttonText, onImportFile }) => {
  const { getRootProps, getInputProps } = useDropzone({
    accept: acceptedTypes,
    onDrop: acceptedFiles => {
      if (acceptedFiles.length > 0) {
        onImportFile(acceptedFiles[0])
      }
    }
  })

  return (
    <div {...getRootProps()}>
      <input {...getInputProps()} />
      <button className="btn" {...buttonProps}>
        <i className="fa fa-download" aria-hidden="true"></i> {buttonText}
      </button>
    </div>
  )
}

FileUploadButton.propTypes = {
  acceptedTypes: PropTypes.arrayOf(PropTypes.string),
  buttonProps: PropTypes.object,
  buttonText: PropTypes.string.isRequired,
  onImportFile: PropTypes.func.isRequired,
}

export default FileUploadButton
