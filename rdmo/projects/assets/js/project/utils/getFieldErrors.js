import { useSelector } from 'react-redux'

export const getFieldErrors = (field) => {
  const errors = useSelector((state) => state.project.errors)
  const errorList = errors?.[0]?.errors?.[field]
  return Array.isArray(errorList) ? errorList : errorList != null ? [errorList] : []
}
