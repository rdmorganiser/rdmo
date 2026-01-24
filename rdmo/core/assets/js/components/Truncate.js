import React, { useRef, useLayoutEffect } from 'react'
import PropTypes from 'prop-types'

const Truncate = ({ text }) => {
  const ref = useRef(null)

  useLayoutEffect(() => {
    const parent = ref.current.parentElement

    const resizeObserver = new ResizeObserver(() => {
      if (ref.current) {
        ref.current.style.width = `${parent.clientWidth}px`
      }
    })

    resizeObserver.observe(parent)

    return () => resizeObserver.disconnect()
  }, [])

  return (
    <span className="truncate" ref={ref}>{text}</span>
  )
}

Truncate.propTypes = {
  text: PropTypes.string.isRequired
}

export default Truncate
