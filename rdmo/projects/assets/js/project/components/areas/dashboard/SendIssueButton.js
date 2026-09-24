import React from 'react'
import PropTypes from 'prop-types'

const SendIssueButton = ({ onClick }) => (
  <button
    type="button"
    className="btn btn-sm p-0 border-0 bg-transparent ms-2"
    onClick={
      (event) => {
        event.stopPropagation()
        onClick()
      }
    }
    aria-label={gettext('Send task')}
    title={gettext('Send task')}
  >
    <i className="bi bi-send" aria-hidden="true" />
  </button>
)

SendIssueButton.propTypes = {
  onClick: PropTypes.func.isRequired,
}

export default SendIssueButton
