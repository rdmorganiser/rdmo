import React from 'react'
import PropTypes from 'prop-types'

const EmptyTableRow = ({ actionLabel, colSpan, message, onAction }) => {
  return (
    <tr>
      <td colSpan={colSpan}>
        <div className="d-flex flex-column align-items-center justify-content-center py-5">
          <p className="text-muted mb-3">{message}</p>
          {
            actionLabel && onAction && (
              <button
                type="button"
                className="btn btn-primary"
                onClick={onAction}
              >
                {actionLabel}
              </button>
            )
          }
        </div>
      </td>
    </tr>
  )
}

EmptyTableRow.propTypes = {
  actionLabel: PropTypes.string,
  colSpan: PropTypes.number.isRequired,
  message: PropTypes.string.isRequired,
  onAction: PropTypes.func,
}

export default EmptyTableRow
