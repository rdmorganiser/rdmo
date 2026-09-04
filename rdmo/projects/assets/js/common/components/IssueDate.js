import PropTypes from 'prop-types'

import { formatDate } from 'rdmo/core/assets/js/utils/date'

const IssueDate = ({ date }) => {
  const { start_date: startDate, end_date: endDate } = date

  if (startDate && endDate) {
    return `${formatDate(startDate, 'long')} - ${formatDate(endDate, 'long')}`
  }

  return startDate ? (
    `${gettext('Start date')}: ${formatDate(startDate, 'long')}`
  ) : `${gettext('End date')}: ${formatDate(endDate, 'long')}`
}

IssueDate.propTypes = {
  date: PropTypes.shape({
    start_date: PropTypes.string,
    end_date: PropTypes.string,
  }).isRequired,
}

export default IssueDate
