import { formatDate } from 'rdmo/core/assets/js/utils/date'

export const renderIssueDate = (date) => {
  const { start_date: startDate, end_date: endDate } = date

  if (startDate && endDate) {
    return `${formatDate(startDate, 'long')} - ${formatDate(endDate, 'long')}`
  }

  return startDate ? (
    `${gettext('Start date')}: ${formatDate(startDate, 'long')}`
  ) : `${gettext('End date')}: ${formatDate(endDate, 'long')}`
}

export default renderIssueDate
