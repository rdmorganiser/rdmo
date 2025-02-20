import React, { useRef, useLayoutEffect } from 'react'
import PropTypes from 'prop-types'
import { isEmpty } from 'lodash'

const Html = ({ html = '' }) => {
  const ref = useRef()

  // if html contains any element with `data-execute="true"`, it will be executed
  // using the method in https://macarthur.me/posts/script-tags-in-react/
  useLayoutEffect(() => {
    if (ref.current && !isEmpty(ref.current.querySelectorAll('[data-execute="true"]'))) {
      // create a range objectm, set it contain the referenced node
      // and create a new fragment with the html code within that range
      const range = document.createRange()
      range.selectNode(ref.current)
      const documentFragment = range.createContextualFragment(html)

      // remove the rendered html and inject it again, triggering a re-run of the JS code
      ref.current.innerHTML = ''
      ref.current.append(documentFragment)
    }
  }, [html])

  return !isEmpty(html) && (
    <div ref={ref} dangerouslySetInnerHTML={{ __html: html }} />
  )
}

Html.propTypes = {
  className: PropTypes.string,
  html: PropTypes.string
}

export default Html
