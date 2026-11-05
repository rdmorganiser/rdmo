import { actions } from '../reducers/errorsSlice'
import { serializeError } from '../utils/errors'

export function setError(key, error, title) {
  return actions.setError({
    key,
    error: { ...serializeError(error), title }
  })
}

export function clearError(key) {
  return actions.clearError(key)
}

export function clearErrors() {
  return actions.clearErrors()
}
