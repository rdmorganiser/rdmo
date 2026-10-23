import React from 'react'
import { useSelector } from 'react-redux'
import { isEmpty } from 'lodash'

import Html from 'rdmo/core/assets/js/components/Html'

const PageHelp = () => {
  const page = useSelector((state) => state.interview.page)

  return !isEmpty(page.help) && (
    <div className="project-interview-page-help" >
      <Html html={page.help} />
    </div>
  )
}

export default PageHelp
