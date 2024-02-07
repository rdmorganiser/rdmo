import React, { useState } from 'react'
import PropTypes from 'prop-types'
import isNil from 'lodash/isNil'

const UploadForm = ({ onSubmit }) => {
  const [file, setFile] = useState(null)

  const handleSubmit = event => {
    event.preventDefault()
    onSubmit(file)
  }

  return (
    <form className="upload-form sidebar-form" onSubmit={handleSubmit}>
      <div className="upload-form-field">
        <input type="file" name="uploaded_file" onChange={event => setFile(event.target.files[0])} accept=".xml"/>
        <p>{file ? file.name : gettext('Select file')}</p>
      </div>

      <div className="sidebar-form-button">
        <button type="submit" className="btn btn-primary" disabled={isNil(file)}
          title={gettext('Upload')} onClick={handleSubmit}>
          <i className="fa fa-arrow-right"></i>
        </button>
      </div>
    </form>
  )
}

UploadForm.propTypes = {
  onSubmit: PropTypes.func.isRequired
}

export { UploadForm }
