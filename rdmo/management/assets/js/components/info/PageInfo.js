import React from 'react'
import PropTypes from 'prop-types'

import { ExtendLink, CodeLink } from '../common/Links'

import useBool from '../../hooks/useBool'

const PageInfo = ({ page, elements, elementActions }) => {

  const [extendSections, toggleSections] = useBool(false)

  const sections = elements.sections.filter(e => page.sections.includes(e.id))

  const fetchSection = (section) => elementActions.fetchElement('sections', section.id)

  return (
    <div className="element-info">
      <p>
        <span dangerouslySetInnerHTML={{
          __html: interpolate(ngettext(
            'This page is used in <b>one section</b>.',
            'This page is used in <b>%s sections</b>.',
            sections.length), [sections.length])}} />
        {sections.length > 0 && <ExtendLink extend={extendSections} onClick={toggleSections} />}
      </p>
      {
        extendSections && sections.map((section, index) => (
          <p key={index}>
            <CodeLink className="code-questions" uri={section.uri} onClick={() => fetchSection(section)} />
          </p>
        ))
      }
    </div>
  )
}

PageInfo.propTypes = {
  page: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default PageInfo
