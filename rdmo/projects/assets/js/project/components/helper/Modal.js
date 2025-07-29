import React, { useEffect, useRef } from 'react'
import PropTypes from 'prop-types'
import { Modal as BootstrapModal } from 'bootstrap'

const Modal = ({
  title,
  show,
  onClose,
  onSubmit,
  submitLabel,
  submitProps,
  children,
  modalProps = {},
  size = ''
}) => {
  const modalRef = useRef(null)
  const modalInstanceRef = useRef(null)

  useEffect(() => {
    const modalEl = modalRef.current
    if (!modalEl) return

    modalInstanceRef.current = BootstrapModal.getOrCreateInstance(modalEl, {
      backdrop: 'static',
      keyboard: true,
      ...modalProps
    })

    if (show) {
      modalInstanceRef.current.show()
    } else {
      modalInstanceRef.current.hide()
    }

    return () => {
      modalInstanceRef.current?.hide()
    }
  }, [show])

  return (
    <div
      ref={modalRef}
      className="modal fade"
      tabIndex="-1"
      aria-hidden={!show}
    >
      <div className={`modal-dialog ${size}`}>
        <div className="modal-content element-modal">
          <div className="modal-header">
            <h2 className="modal-title">{title}</h2>
            <button
              type="button"
              className="btn-close"
              onClick={onClose}
              aria-label={gettext('Close')}
            ></button>
          </div>

          {children && (
            <div className="modal-body">
              {children}
            </div>
          )}

          <div className="modal-footer">
            {onSubmit && (
              <button
                type="button"
                className="btn btn-primary"
                onClick={onSubmit}
                {...submitProps}
              >
                {submitLabel ?? gettext('Save')}
              </button>
            )}
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onClose}
            >
              {gettext('Cancel')}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

Modal.propTypes = {
  title: PropTypes.string.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func,
  submitLabel: PropTypes.string,
  submitProps: PropTypes.object,
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node
  ]),
  modalProps: PropTypes.object,
  size: PropTypes.string
}

export default Modal
