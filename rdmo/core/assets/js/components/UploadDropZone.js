import React,  { useState } from 'react'
import PropTypes from 'prop-types'
import { useDropzone } from 'react-dropzone'

const UploadDropZone = ({ acceptedTypes, onImportFile }) => {
  const [errorMessage, setErrorMessage] = useState('')

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: acceptedTypes,
    onDropAccepted: acceptedFiles => {
      if (acceptedFiles.length > 0) {
        onImportFile(acceptedFiles[0])
        setErrorMessage('')
      }
    },
    onDropRejected: rejectedFiles => {
      setErrorMessage(interpolate(gettext('%s has unsupported file type'), [rejectedFiles[0].path]))
    }
  })

  return (
    <section className="dropzone-container">
      <div {...getRootProps({className: 'dropzone'})}>
        <input {...getInputProps()} />
        {
          isDragActive ? (
            <div>
              {gettext('Drop the file here ...')}
            </div>
          ) : (
            <div>
              {gettext('Drag and drop a file here or click to select a file')}
            </div>
          )
        }
        {errorMessage && <div className="alert alert-danger mt-2">{errorMessage}</div>}
      </div>
    </section>
  )
}

UploadDropZone.propTypes = {
  acceptedTypes: PropTypes.arrayOf(PropTypes.string),
  onImportFile: PropTypes.func.isRequired,
}

export default UploadDropZone
