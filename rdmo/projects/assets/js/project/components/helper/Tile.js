import React from 'react'
import PropTypes from 'prop-types'

const Tile = ({ title, children, className = '', size = 'normal', style = 'normal', href, onClick }) => {
  const sizeClasses = {
    compact: 'col-12 col-md-4',  // 3 tiles per row
    normal: 'col-12 col-md-6',   // 2 tiles per row
    fullWidth: 'col-12',         // 1 tile per row
  }

  const tileStyleClass = style === 'warning' ? 'tile-warning' : ''

  const card = (
    <div
      className={`card border-0 bg-white rounded-3 shadow-sm p-0 ${tileStyleClass}`}
      style={href || onClick ? { cursor: 'pointer' } : undefined}
      onClick={onClick}
    >
      <div className="card-body">
        {children}
      </div>
    </div>
  )

  return (
    <div className={`mb-4 ${sizeClasses[size]} ${className}`}>
      {title && <h2 className="fw-bold mb-2">{title}</h2>}
      {href ? (
        <a href={href} className="text-decoration-none d-block">
          {card}
        </a>
      ) : (
        card
      )}
    </div>
  )
}

Tile.propTypes = {
  title: PropTypes.string,
  children: PropTypes.node.isRequired,
  className: PropTypes.string,
  size: PropTypes.oneOf(['compact', 'normal', 'fullWidth']),
  style: PropTypes.oneOf(['normal', 'warning']),
  href: PropTypes.string,
  onClick: PropTypes.func,
}

export default Tile
