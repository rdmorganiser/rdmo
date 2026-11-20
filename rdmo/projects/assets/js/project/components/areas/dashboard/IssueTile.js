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
        className={classNames('card card-tile h-100', { 'cursor-pointer': onCardClick })}
        onClick={onCardClick}
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
  label: PropTypes.node,
  buttonLabel: PropTypes.node,
  buttonClassName: PropTypes.string,
  buttonIconClassName: PropTypes.string,
  children: PropTypes.node,
  className: PropTypes.string,
  onClick: PropTypes.func,
  onCardClick: PropTypes.func
}

export default IssueTile
