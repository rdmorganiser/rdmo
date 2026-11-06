import { useCallback } from 'react'

import useConfig from './useConfig'

const useConfigToggle = (path, defaultValue = false) => {
  const [value, setValue] = useConfig(path, defaultValue)
  const toggleValue = useCallback(() => setValue(!value), [setValue, value])

  return [value, toggleValue]
}

export default useConfigToggle
