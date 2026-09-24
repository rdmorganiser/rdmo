import React from 'react'
import { useSelector } from 'react-redux'
import { isEmpty, isNil } from 'lodash'

import ElementsSidebar from '../components/sidebar/ElementsSidebar'
import ImportSidebar from '../components/sidebar/ImportSidebar'

const Sidebar = () => {
  const config = useSelector((state) => state.config)
  const imports = useSelector((state) => state.imports)

  // check if anything was loaded yet
  if (isNil(config.settings)) {
    return null
  }

  if (isEmpty(imports.elements)) {
    return <ElementsSidebar />
  } else {
    return <ImportSidebar />
  }
}

export default Sidebar
