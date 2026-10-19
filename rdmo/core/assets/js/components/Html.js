import React, { useLayoutEffect, useRef } from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'
import { isEmpty } from 'lodash'

const Html = ({ id = null, className = '', html = '' }) => {
  const ref = useRef()
  const settings = useSelector((state) => state.settings)

  // if html contains a <script> tag, and settings.TEMPLATES_EXECUTE_SCRIPT_TAGS is True,
  // it will be executed using the method in https://macarthur.me/posts/script-tags-in-react/
  if (settings.templates_execute_script_tags) {
    useLayoutEffect(() => {
      if (ref.current) {
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
  }

  return !isEmpty(html) && (
    <span ref={ref} id={id} className={className} dangerouslySetInnerHTML={{ __html: html }} />
  )
}

Html.propTypes = {
  id: PropTypes.string,
  className: PropTypes.string,
  html: PropTypes.string
}

export default Html
