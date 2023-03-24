import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { ExtendLink } from '../common/Links'

import useBool from '../../hooks/useBool'

const PageInfo = ({ page, elements }) => {

  const [extendSections, toggleSections] = useBool(false)

  const sections = elements.sections.filter(e => page.sections.includes(e.id))

  return (
    <div className="element-info">
      {
        sections.length > 0 && <>
          <p>
            <span dangerouslySetInnerHTML={{
              __html: interpolate(ngettext(
                'This page is used in <b>one section</b>.',
                'This page is used in <b>%s sections</b>.',
                sections.length), [sections.length])}} />
            <ExtendLink extend={extendSections} onClick={toggleSections} />
          </p>
          {
            extendSections && sections.map((section, index) => (
              <p key={index}>
                <code className="code-questions">{section.uri}</code>
              </p>
            ))
          }
        </>
      }
    </div>
  )
}

PageInfo.propTypes = {
  page: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired
}

export default PageInfo
