import { useMemo } from 'react'
import { useSelector } from 'react-redux'

const EMPTY_ERRORS = {}

export const useFieldErrors = () => {
  const rawErrors = useSelector((state) => state.project.errors?.[0]?.errors) || EMPTY_ERRORS

  // Optional but recommended: avoid allocating a new object if rawErrors didn't change
  return useMemo(() => (
    Object.fromEntries(
      Object.entries(rawErrors).map(([field, err]) => [
        field,
        Array.isArray(err) ? err : err != null ? [err] : []
      ])
    )
  ), [rawErrors])
}
