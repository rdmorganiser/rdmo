import { isNil } from 'lodash'

const isReady = (interview) => {
  return (
    (interview.done && !isNil(interview.navigation)) ||
    (interview.page && !isNil(interview.navigation) && !isNil(interview.values))
  )
}

export { isReady }
