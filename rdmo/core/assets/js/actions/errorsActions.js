import { actions } from '../reducers/errorsSlice'
import { serializeError } from '../utils/errors'

export function setError(source, error, context) {
  return actions.setError({
    source,
    error: { ...serializeError(error), context }
  })
}

export function clearError(source) {
  return actions.clearError(source)
}

export function clearErrors() {
  return actions.clearErrors()
}
