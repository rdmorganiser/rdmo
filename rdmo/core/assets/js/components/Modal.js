import React, { useEffect, useRef } from 'react'
import PropTypes from 'prop-types'
import { Modal as BootstrapModal } from 'bootstrap'

const Modal = ({
  title,
  show,
  onClose,
  closeLabel,
  onSubmit,
  onShown,
  submitLabel,
  submitProps,
  children,
  modalProps = {},
  size = '',
  extraButtons = null
}) => {
  const modalRef = useRef(null)

  useEffect(() => {
    const modalElement = modalRef.current
    if (!modalElement) return

    const modal = BootstrapModal.getOrCreateInstance(modalElement, {
      backdrop: 'static',
      keyboard: true,
      ...modalProps
    })

    const handleHide = () => {
      if (show) {
        onClose()
      }
    }

    modalElement.addEventListener('shown.bs.modal', onShown)
    modalElement.addEventListener('hide.bs.modal', handleHide)

    if (show) {
      modal.show()
    }

    return () => {
      modalElement.removeEventListener('shown.bs.modal', onShown)
      modalElement.removeEventListener('hide.bs.modal', handleHide)
      modal.hide()
    }
  }, [show])

  return (
    <div ref={modalRef} className="modal fade" tabIndex="-1" aria-hidden={!show}>
      <div className={`modal-dialog ${size}`}>
        <div className="modal-content element-modal">
          <div className="modal-header">
            <h2 className="modal-title">{title}</h2>
            <button type="button" className="btn-close" onClick={onClose} aria-label={gettext('Close')}></button>
          </div>

          {
            children && (
              <div className="modal-body">
                {children}
              </div>
            )
          }

          <div className="modal-footer">
            {extraButtons}
            {
              onSubmit && (
                <button type="button" className="btn btn-primary" onClick={onSubmit} {...submitProps}>
                  {submitLabel ?? gettext('Save')}
                </button>
              )
            }
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              {closeLabel ?? gettext('Cancel')}
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
  onShown: PropTypes.func,
  submitLabel: PropTypes.node,
  closeLabel: PropTypes.string,
  submitProps: PropTypes.object,
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node
  ]),
  modalProps: PropTypes.object,
  size: PropTypes.string,
  extraButtons: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node
  ]),
}

export default Modal
