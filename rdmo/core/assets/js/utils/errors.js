// Copy errors at the Redux boundary; callers can still receive the original error.
export const serializeError = (error) => {
  if (error === null || typeof error !== 'object' || Array.isArray(error)) {
    return error
  }

  // API error fields, including JSON validation details, are enumerable.
  const result = { ...error }
  const errorType = error.constructor?.name
  if (typeof errorType === 'string' && errorType !== 'Object') {
    result.errorType = errorType
  }

  // Native Error diagnostics are not enumerable and need copying explicitly.
  for (const key of ['name', 'message', 'stack']) {
    if (typeof error[key] === 'string') {
      result[key] = error[key]
    }
  }

  return result
}

// Validation details can nest message strings inside arrays and field-name objects.
// Recursively flatten these into a message list, discarding the field names.
const collectErrorMessages = (details) => {
  if (typeof details === 'string') return [details]
  if (details && typeof details === 'object') {
    return Object.values(details).flatMap(collectErrorMessages)
  }
  // Ignore null and non-string scalar values.
  return []
}

export const getErrorMessages = (error) => {
  // Handle absent errors and message-only inputs before inspecting structured errors.
  if (error == null) return []
  if (typeof error === 'string' || Array.isArray(error)) return collectErrorMessages(error)

  // Prefer backend validation details over generic request diagnostics.
  const messages = collectErrorMessages(error.errors)
  if (messages.length) return messages

  // Fall back to the native error message, HTTP status text, then a translated default.
  const message = error.message || error.statusText || gettext('An unknown error occurred, please contact support')
  return [message]
}
