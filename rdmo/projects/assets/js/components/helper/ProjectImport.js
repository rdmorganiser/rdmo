import React from 'react'
import PropTypes from 'prop-types'

import { UploadDropZone } from 'rdmo/core/assets/js/components'

const ProjectImport = ({ allowedTypes, handleImport, importUrls}) => {

  const renderDirectImportLinks = () => {
    return (
      <div className="mt-10">
        <label className="control-label">{gettext('Import directly')}</label>
        <ul className='list-unstyled mb-0'>
        {importUrls.map((url) => (
          <li key={url.key}>
            <a href={url.href} target='_blank' rel='noopener noreferrer'>
              {url.label}
            </a>
          </li>
        ))}
        </ul>
      </div>
    )
  }

  return (
    <>
      <label className="control-label">{gettext('Import from file')}</label>
      <UploadDropZone
        acceptedTypes={allowedTypes}
        onImportFile={handleImport} />
        {importUrls.length > 0 && renderDirectImportLinks()}
    </>
  )
}

ProjectImport.propTypes = {
  allowedTypes: PropTypes.arrayOf(PropTypes.string),
  handleImport: PropTypes.func.isRequired,
  importUrls: PropTypes.arrayOf(PropTypes.object).isRequired
}

export default ProjectImport
