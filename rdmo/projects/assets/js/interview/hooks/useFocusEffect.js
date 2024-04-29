import { isNil } from 'lodash'

import { useEffect } from 'react'

const useFocusEffect = (ref, dependencies, focus) => {
  useEffect(() => {
    if ((isNil(focus) || focus) && !isNil(ref.current)) {
      const timeout = setTimeout(() => {
        ref.current.focus()
      }, 200)

      return () => {
        // clears timeout before running the new effect
        clearTimeout(timeout)
      }
    }
  }, [...dependencies, isNil(focus) || focus])
}

export default useFocusEffect
