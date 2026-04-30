import React from 'react'
import PropTypes from 'prop-types'

const Tile = ({ title, label, buttonLabel, children, className = '', size = 'normal', onClick, onCardClick }) => {
  const sizeClasses = {
    compact: 'col-12 col-md-4',  // 3 tiles per row
    normal: 'col-12 col-md-6',   // 2 tiles per row
    fullWidth: 'col-12',         // 1 tile per row
  }

  return (
    <div
      className={`card card-tile mb-4 rounded-3 ${sizeClasses[size]} ${className}`}
      onClick={onCardClick}
      style={onCardClick ? { cursor: 'pointer' } : undefined} >
      <div className="card-body d-flex flex-column">
        {label && <div className="text-success fw-semibold small mb-1">{label}</div>}
        {title && <h3 className="card-title mb-2">{title}</h3>}
        <div className="card-text mb-2">{children}</div>

        {
          onClick && buttonLabel && (
            <div className="mt-auto">
              <button
                type="button"
                className="btn btn-outline-secondary"
                // onClick={onClick}
                onClick={
                  (e) => {
                    e.stopPropagation()
                    onClick()
                  }
                }
              >
                {buttonLabel} <span className="ms-1">→</span>
              </button>
            </div>
          )
        }
      </div>
    </div>
  )
}

Tile.propTypes = {
  title: PropTypes.string,
  buttonLabel: PropTypes.node,
  children: PropTypes.node,
  className: PropTypes.string,
  label: PropTypes.node,
  size: PropTypes.oneOf(['compact', 'normal', 'fullWidth']),
  onClick: PropTypes.func,
  onCardClick: PropTypes.func
}

export default Tile
