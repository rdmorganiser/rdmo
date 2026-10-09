import React from 'react'
import PropTypes from 'prop-types'

const EmptyTableRow = ({ label, colSpan, message, onClick }) => {
  return (
    <tr>
      <td colSpan={colSpan}>
        <div className="d-flex flex-column align-items-center justify-content-center py-5">
          <p className="text-muted mb-3">{message}</p>
          {
            label && onClick && (
              <button
                type="button"
                className="btn btn-primary"
                onClick={onClick}
              >
                {label}
              </button>
            )
          }
        </div>
      </td>
    </tr>
  )
}

EmptyTableRow.propTypes = {
  label: PropTypes.string,
  colSpan: PropTypes.number.isRequired,
  message: PropTypes.string.isRequired,
  onClick: PropTypes.func,
}

export default EmptyTableRow
