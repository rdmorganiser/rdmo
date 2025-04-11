import { isEmpty, isNil } from 'lodash'

const isReady = (interview) => {
  return (
    (interview.done && !isNil(interview.navigation)) ||
    (interview.page && !isNil(interview.navigation) && !isNil(interview.values))
  )
}

const hasErrors = (project, interview) => {
  return !(isEmpty(project.errors) && isEmpty(interview.errors))
}

export { isReady, hasErrors }
