import isUndefined from 'lodash/isUndefined'

const showInterview = (interview) => {
  return !isUndefined(interview.page) && !isUndefined(interview.navigation) && !isUndefined(interview.values)
}

export { showInterview }
