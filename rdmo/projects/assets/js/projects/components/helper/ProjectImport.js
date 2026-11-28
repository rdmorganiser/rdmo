import React from 'react'
import PropTypes from 'prop-types'
import { isEmpty } from 'lodash'

import { getErrorMessages } from 'rdmo/core/assets/js/utils/errors'

import Dropzone from 'rdmo/core/assets/js/components/Dropzone'

const ProjectImport = ({ uploadAccept, formImports, uploadError, onUpload, onImport }) => {
  return (
    <>
      <label className="form-label">{gettext('Import from file')}</label>
      <Dropzone
        acceptedTypes={uploadAccept}
        onDrop={onUpload} />
      {
        getErrorMessages(uploadError).map((message, index) => (
          <div key={index} className="alert alert-danger mt-2 mb-0">{message}</div>
        ))
      }
      {
        !isEmpty(formImports) && (
          <div className="mt-3">
            <label className="form-label">{gettext('Import directly')}</label>
            <ul className="list-unstyled mb-0">
              {
                formImports.map(([key, { label }]) => (
                  <li key={key}>
                    <button type="button" className="link" onClick={() => onImport(key)}>
                      {label}
                    </button>
                  </li>
                ))
              }
            </ul>
          </div>
        )
      }
    </>
  )
}

ProjectImport.propTypes = {
  uploadAccept: PropTypes.object,
  formImports: PropTypes.array.isRequired,
  uploadError: PropTypes.object,
  onUpload: PropTypes.func.isRequired,
  onImport: PropTypes.func.isRequired
}

export default ProjectImport
