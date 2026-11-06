import React from 'react'
import PropTypes from 'prop-types'

import { Textarea } from 'rdmo/core/assets/js/components/forms'

const SendIssueEmail = ({
  formData,
  setField,
  onCheckboxChange,
  recipientChoices,
  recipientInputEnabled,
  errors
}) => {
  return (
    <>
      <div className="fw-semibold mb-2">{gettext('Recipients')}</div>
      {
        recipientChoices.length > 0 && (
          <div>
            {
              recipientChoices.map(([value, label], index) => (
                <div className="form-check" key={value}>
                  <input
                    id={`id_recipients_${index}`}
                    name="recipients"
                    type="checkbox"
                    className="form-check-input"
                    value={value}
                    checked={formData.recipients.includes(value)}
                    onChange={(event) => onCheckboxChange('recipients', value, event.target.checked)}
                  />
                  <label className="form-check-label fw-normal" htmlFor={`id_recipients_${index}`}>
                    {label}
                  </label>
                </div>
              ))
            }
          </div>
        )
      }
      {
        recipientInputEnabled && (
          <Textarea
            className="mb-3"
            rows="3"
            placeholder={gettext('Enter recipients line by line')}
            value={formData.recipients_input}
            onChange={(value) => setField('recipients_input', value)}
            errors={errors.recipientsInput}
          />
        )
      }
      {
        errors.recipients?.map((error, index) => (
          <div key={index} className="text-danger mt-1">{error}</div>
        ))
      }
    </>
  )
}

SendIssueEmail.propTypes = {
  formData: PropTypes.object.isRequired,
  setField: PropTypes.func.isRequired,
  onCheckboxChange: PropTypes.func.isRequired,
  recipientChoices: PropTypes.array.isRequired,
  recipientInputEnabled: PropTypes.bool.isRequired,
  errors: PropTypes.shape({
    recipients: PropTypes.array,
    recipientsInput: PropTypes.array
  }).isRequired
}

export default SendIssueEmail
