import { useEffect } from 'react'
import { isNil } from 'lodash'

const useFocusEffect = (ref, show) => {
  useEffect(() => {
    if (show && !isNil(ref.current)) {
      const timeout = setTimeout(() => {
        ref.current.focus()
      }, 100)

      return () => {
        // clears timeout before running the new effect
        clearTimeout(timeout)
      }
    }
  }, [show])
}

export default useFocusEffect
