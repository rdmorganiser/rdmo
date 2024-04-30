import { isNil } from 'lodash'

const isReady = (interview) => {
  return !(isNil(interview.page) || isNil(interview.navigation) || isNil(interview.values))
}

export { isReady }
