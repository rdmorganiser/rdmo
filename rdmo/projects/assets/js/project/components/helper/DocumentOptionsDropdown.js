import React from 'react'
import PropTypes from 'prop-types'

import DocumentOptions from './DocumentOptions'

const DocumentOptionsDropdown = ({ areaTag, onChanged }) => {


  return (
    <div className="dropdown dropdown-menu-end">
      <button
        type="button"
        className="link text-nowrap"
        data-bs-toggle="dropdown"
        data-bs-popper-config='{"strategy":"fixed"}'
        aria-expanded="false"
        onClick={(event) => event.stopPropagation()}
        title={gettext('Document Options')}
      >
        <span>{gettext('Document Options')}</span>
        <i className="bi bi-caret-down-fill ms-1" />
      </button>

      <ul
        className="dropdown-menu" onClick={(event) => event.stopPropagation()}
      >
        <DocumentOptions onChanged={onChanged} areaTag={areaTag} />
      </ul>
    </div>
  )
}

DocumentOptionsDropdown.propTypes = {
  areaTag: PropTypes.string.isRequired,
  onChanged: PropTypes.func
}

export default DocumentOptionsDropdown
