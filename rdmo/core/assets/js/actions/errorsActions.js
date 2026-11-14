import { actions } from '../reducers/errorsSlice'
import { serializeError } from '../utils/errors'

export function setError(key, error, title) {
  return actions.setError({
    key,
    error: { ...serializeError(error), title }
  })
}

export function clearError(...keys) {
  return actions.clearError(keys)
}

export function clearErrors() {
  return actions.clearErrors()
}
