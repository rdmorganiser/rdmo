import React from 'react'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

import ExportsDropdown from './ExportsDropdown'
import Tile from './Tile'

const ViewTile = ({ title, help, onClick, onExport }) => (
  <Tile size={'compact'} onClick={onClick}>
    <div className="d-flex">
      <div className="d-flex align-items-center justify-content-center me-3 flex-shrink-0">
        <i className="bi bi-file-earmark-text" />
      </div>

      <div className="flex-grow-1 d-flex flex-column">
        <div className="d-flex justify-content-between align-items-start mb-1">
          <div className="fw-bold">{title}</div>
          <ExportsDropdown onExport={onExport} title={false} />
        </div>

        {help && (
          <div className="text-muted small mb-2">
            <Html html={help} />
          </div>
        )}
      </div>
    </div>
  </Tile>
)

ViewTile.propTypes = {
  title: PropTypes.string.isRequired,
  help: PropTypes.string,
  onClick: PropTypes.func,
  onExport: PropTypes.func
}

export default ViewTile
