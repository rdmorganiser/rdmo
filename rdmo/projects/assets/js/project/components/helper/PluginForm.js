import React, { useRef, useEffect } from 'react'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

const PluginForm = ({ html }) => {
  const ref = useRef(null)

  useEffect(() => {
    if (ref.current) {
      const form = ref.current.querySelector('form')

      const submitForm = (event) => {
        event.preventDefault()

        const formData = new FormData(form)
        console.log(formData.get('input'))
      }

      // add event listener to form
      form.addEventListener('submit', submitForm)

      // cleanup on unmount
      return () => form.removeEventListener('submit', submitForm)
    }
  }, [])

  return <div ref={ref}><Html html={html} /></div>
}

PluginForm.propTypes = {
  html: PropTypes.string
}

export default PluginForm
