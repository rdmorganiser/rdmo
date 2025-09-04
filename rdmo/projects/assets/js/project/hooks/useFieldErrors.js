import { useSelector } from 'react-redux'

export const useFieldErrors = () => {
  const errors = useSelector((state) => state.project.errors?.[0]?.errors ?? {})
  return Object.fromEntries(
    Object.entries(errors).map(([field, err]) => [
      field,
      Array.isArray(err) ? err : err != null ? [err] : []
    ])
  )
}
