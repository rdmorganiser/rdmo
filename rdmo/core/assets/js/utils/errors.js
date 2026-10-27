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
