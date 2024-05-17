import { isNil } from 'lodash'

import { useEffect } from 'react'

const useFocusEffect = (ref, show) => {
  useEffect(() => {
    if (show && !isNil(ref.current)) {
      const timeout = setTimeout(() => {
        ref.current.focus()
      }, 200)

      return () => {
        // clears timeout before running the new effect
        clearTimeout(timeout)
      }
    }
  }, [show])
}

export default useFocusEffect
