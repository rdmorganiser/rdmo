import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const IssueTile = ({
  title,
  label,
  buttonLabel,
  buttonClassName = 'btn-outline-primary',
  buttonIconClassName,
  children,
  className,
  onClick,
  onCardClick
}) => {
  return (
    <div className={classNames(className)}>
      <div
        className="card card-tile cursor-pointer h-100"
        onClick={onCardClick}
        style={onCardClick ? { cursor: 'pointer' } : undefined}
      >
        <div className="card-body d-flex flex-column">
          {
            label && <strong className="text-secondary small mb-2">{label}</strong>
          }
          {
            title && <h3 className="card-title mb-3">{title}</h3>
          }

          <div className="card-text">{children}</div>

          {
            onClick && buttonLabel && (
              <div className="mt-auto">
                <button
                  type="button"
                  className={classNames('btn', buttonClassName)}
                  onClick={
                    (e) => {
                      e.stopPropagation()
                      onClick()
                    }
                  }
                >
                  <>
                    {buttonLabel}
                    {
                      buttonIconClassName && (
                        <i className={classNames(buttonIconClassName, 'ms-1')} />
                      )
                    }
                  </>
                </button>
              </div>
            )
          }
        </div>
      </div>
    </div>
  )
}

IssueTile.propTypes = {
  title: PropTypes.string,
  buttonLabel: PropTypes.node,
  buttonClassName: PropTypes.string,
  buttonIconClassName: PropTypes.string,
  children: PropTypes.node,
  className: PropTypes.string,
  label: PropTypes.node,
  size: PropTypes.oneOf(['compact', 'normal', 'fullWidth']),
  onClick: PropTypes.func,
  onCardClick: PropTypes.func
}

export default IssueTile
