import React from 'react'
import { useSelector } from 'react-redux'
import PropTypes from 'prop-types'

import Tabs from './Tabs'

const LanguageTabs = ({ render }) => {
  const { settings } = useSelector((state) => state.config)

  const labels = settings.languages.map(([, lang]) => lang)
  const tabs = settings.languages.map(([lang_code]) => render(lang_code))

  return settings && <Tabs labels={labels} tabs={tabs} />
}

LanguageTabs.propTypes = {
  render: PropTypes.func,
}

export default LanguageTabs
