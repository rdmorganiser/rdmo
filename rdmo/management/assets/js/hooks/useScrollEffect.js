import { useEffect } from 'react'
import isNil from 'lodash/isNil'

const useScrollEffect = (elementType, elementId, elementAction) => {
  useEffect(() => {
    let lsKey = `rdmo.management.scroll.${elementType}`
    if (!isNil(elementId)) {
      lsKey += `.${elementId}`
    }
    if (!isNil(elementAction)) {
      lsKey += `.${elementAction}`
    }
    const lsValue = localStorage.getItem(lsKey, 0)

    // scroll to the right position
    setTimeout(() => window.scrollTo(0, lsValue), 0)

    // add a event handler to store the scroll position
    const handleScroll = () => {
      const lsValue = window.pageYOffset
      localStorage.setItem(lsKey, lsValue)
    }
    window.addEventListener('scroll', handleScroll)
    return () => {
      window.removeEventListener('scroll', handleScroll)
    }

  }, [elementType, elementId, elementAction])
}

export default useScrollEffect
