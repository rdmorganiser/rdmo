import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

import { fetchElement } from '../../actions/elementActions'

import { ExtendLink, CodeLink } from '../common/Links'

import useBool from '../../hooks/useBool'

const PageInfo = ({ page }) => {
  const dispatch = useDispatch()

  const elements = useSelector((state) => state.elements)

  const [extendSections, toggleSections] = useBool(false)

  const sections = elements.sections.filter(e => page.sections.includes(e.id))

  const fetchSection = (section) => dispatch(fetchElement('sections', section.id))

  return (
    <div className="mb-2">
      <p className="mb-1">
        <Html html={interpolate(ngettext(
          'This page is used in <b>one section</b>.',
          'This page is used in <b>%s sections</b>.',
          sections.length), [sections.length])} />
        {sections.length > 0 && <ExtendLink extend={extendSections} onClick={toggleSections} />}
      </p>
      {
        extendSections && sections.map((section, index) => (
          <p className="mb-1" key={index}>
            <CodeLink className="code-questions" uri={section.uri} onClick={() => fetchSection(section)} />
          </p>
        ))
      }
    </div>
  )
}

PageInfo.propTypes = {
  page: PropTypes.object.isRequired
}

export default PageInfo
