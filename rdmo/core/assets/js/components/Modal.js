import React, { useEffect, useRef } from 'react'
import PropTypes from 'prop-types'
import { Modal as BootstrapModal } from 'bootstrap'
import classNames from 'classnames'

const Modal = ({
  show,
  size = 'lg',
  modalProps = {},
  title,
  children,
  footerChildren = null,
  closeLabel,
  submitLabel,
  submitProps,
  onShown,
  onClose,
  onSubmit
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

  const dialogClassName = classNames('modal-dialog', {
    [`modal-${size}`]: size !== 'md'
  })

  return (
    <div ref={modalRef} className="modal fade" tabIndex="-1" aria-hidden={!show}>
      <div className={dialogClassName}>
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
            {footerChildren}

            <button type="button" className="btn btn-secondary" onClick={onClose}>
              {closeLabel ?? gettext('Close')}
            </button>
            {
              onSubmit && (
                <button type="button" className="btn btn-primary" onClick={onSubmit} {...submitProps}>
                  {submitLabel ?? gettext('Submit')}
                </button>
              )
            }
          </div>
        </div>
      </div>
    </div>
  )
}

Modal.propTypes = {
  show: PropTypes.bool.isRequired,
  size: PropTypes.oneOf(['sm', 'md', 'lg', 'xl']),
  modalProps: PropTypes.object,
  title: PropTypes.string.isRequired,
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node
  ]),
  footerChildren: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node
  ]),
  closeLabel: PropTypes.node,
  submitLabel: PropTypes.node,
  submitProps: PropTypes.object,
  onShown: PropTypes.func,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func
}

export default Modal
