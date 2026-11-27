import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { isEmpty } from 'lodash'

import { getErrorMessages } from 'rdmo/core/assets/js/utils/errors'

import Dropzone from 'rdmo/core/assets/js/components/Dropzone'

import { downloadExport } from '../../actions/exportActions'
import { uploadImport } from '../../actions/importActions'
import { navigateDashboard } from '../../actions/navigationActions'
import { combineUploadAccept } from '../../utils/import'
import { IssueTile } from '../helper'

const Transfer = () => {
  const dispatch = useDispatch()

  const exportList = useSelector((state) => state.export.exportList) ?? {}
  const importList = useSelector((state) => state.import.importList) ?? {}
  const uploadError = useSelector((state) => state.import.uploadError)

  const formImports = Object.entries(importList).filter(([, { upload }]) => !upload)
  const uploadImports = Object.entries(importList).filter(([, { upload }]) => upload)

  const handleUpload = (file) => {
    dispatch(uploadImport(file)).then((response) => {
      // the upload returns the key of the plugin, which accepted the file
      if (response?.key) {
        dispatch(navigateDashboard({ area: 'transfer', importKey: response.key }))
      }
    })
  }

  const uploadAccept = combineUploadAccept(uploadImports)

  return (
    <div className="project-transfer">
      <h1 className="mb-5">{gettext('Export / Import')}</h1>

      {
        !isEmpty(exportList) && (
          <div className="project-transfer-exports mb-4">
            <h2>{gettext('Export')}</h2>
            <div className="row">
              {
                Object.entries(exportList).map(([key, { label, description, download }]) => (
                  <IssueTile
                    key={key}
                    className="col-lg-4 mb-4"
                    title={label}
                    buttonLabel={download ? gettext('Download') : gettext('Export')}
                    buttonClassName="btn-primary"
                    buttonIconClassName={download ? 'bi bi-download' : 'bi bi-arrow-right'}
                    onClick={
                      () => dispatch(
                        download ? downloadExport(key) : navigateDashboard({ area: 'transfer', exportKey: key })
                      )
                    }
                  >
                    <p className="text-secondary">{description}</p>
                  </IssueTile>
                ))
              }
            </div>
          </div>
        )
      }

      {
        !(isEmpty(formImports) && isEmpty(uploadImports)) && (
          <div className="project-transfer-imports mb-4">
            <h2>{gettext('Import')}</h2>
            <div className="row">
              {
                formImports.map(([key, { label, description }]) => (
                  <IssueTile
                    key={key}
                    className="col-lg-4 mb-4"
                    title={label}
                    buttonLabel={gettext('Import')}
                    buttonClassName="btn-primary"
                    buttonIconClassName="bi bi-arrow-right"
                    onClick={() => dispatch(navigateDashboard({ area: 'transfer', importKey: key }))}
                  >
                    <p className="text-secondary">{description}</p>
                  </IssueTile>
                ))
              }
              {
                !isEmpty(uploadImports) && (
                  <IssueTile
                    className="col-lg-4 mb-4"
                    title={gettext('Upload')}
                  >
                    <p className="text-secondary">
                      {gettext('Import from a file, which is uploaded from your computer.')}
                    </p>
                    <Dropzone
                      label={gettext('Drop or select a file')}
                      acceptedTypes={uploadAccept}
                      onDrop={handleUpload}
                    />
                    {
                      getErrorMessages(uploadError).map((message, index) => (
                        <div key={index} className="alert alert-danger mt-2 mb-0">{message}</div>
                      ))
                    }
                  </IssueTile>
                )
              }
            </div>
          </div>
        )
      }
    </div>
  )
}

export default Transfer
