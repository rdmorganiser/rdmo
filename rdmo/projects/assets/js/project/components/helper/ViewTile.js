import React from 'react'
import PropTypes from 'prop-types'

import Img from 'rdmo/core/assets/js/components/Img'
import Truncate from 'rdmo/core/assets/js/components/Truncate'

import ExportsDropdown from './ExportsDropdown'

const ViewTile = ({ title, help, onClick, onExport }) => (
  <div className="card card-tile cursor-pointer mb-4" onClick={onClick}>
    <div className="d-flex">
      <Img src="/core/img/document.png" className="img-fluid" alt={gettext('Document image')} />
      <div className="card-body overflow-hidden">
        <div className="d-flex flex-column justify-content-center h-100 foo">
          <div>
            <h3 className="card-title mb-2">
              <Truncate text={title} selector=".card-body" />
            </h3>
            <p className="card-text text-muted mb-2">
              <Truncate text={help} selector=".card-body" />
            </p>
            <ExportsDropdown onExport={onExport} />
          </div>
        </div>
      </div>
    </div>
  </div>
)

ViewTile.propTypes = {
  title: PropTypes.string.isRequired,
  help: PropTypes.string,
  onClick: PropTypes.func,
  onExport: PropTypes.func
}

export default ViewTile
