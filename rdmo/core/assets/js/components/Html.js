import React, { useRef, useLayoutEffect } from 'react'
import PropTypes from 'prop-types'
import { isEmpty } from 'lodash'

import { executeScriptTags } from 'rdmo/core/assets/js/utils/meta'


const Html = ({ html = '' }) => {
  const ref = useRef()

  // if html contains a <script> tag, and settings.TEMPLATES_EXECUTE_SCRIPT_TAGS is True,
  // it will be executed using the method in https://macarthur.me/posts/script-tags-in-react/
  if (executeScriptTags) {
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
    <span ref={ref} dangerouslySetInnerHTML={{ __html: html }} />
  )
}

Html.propTypes = {
  className: PropTypes.string,
  html: PropTypes.string
}

export default Html
