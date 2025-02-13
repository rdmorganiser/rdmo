import React from 'react'
import PropTypes from 'prop-types'

const Tile = ({ title, children, className = '', size = 'normal' }) => {
  const sizeClasses = {
    compact: 'col-12 col-md-4',  // 3 tiles per row
    normal: 'col-12 col-md-6',   // 2 tiles per row
    fullWidth: 'col-12',         // 1 tile per row
  }

  return (
    <div className={`mb-4 ${sizeClasses[size]} ${className}`}>
      {title && <h5 className="fw-bold mb-2">{title}</h5>}

      <div className="card border-0 bg-white rounded-3 shadow-sm p-0">
        <div className="card-body">{children}</div>
      </div>
    </div>
  )
}

Tile.propTypes = {
  title: PropTypes.string,
  children: PropTypes.node.isRequired,
  className: PropTypes.string,
  size: PropTypes.oneOf(['compact', 'normal', 'fullWidth']),
}

export default Tile
