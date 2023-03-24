import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { ExtendLink } from '../common/Links'

import useBool from '../../hooks/useBool'

const SectionInfo = ({ section, elements }) => {

  const [showCatalogs, toggleCatalogs] = useBool(false)

  const catalogs = elements.catalogs.filter(e => section.catalogs.includes(e.id))

  return (
    <div className="element-info">
      {
        catalogs.length > 0 && <>
          <p>
            <span dangerouslySetInnerHTML={{
              __html: interpolate(ngettext(
                'This section is used in <b>one catalog</b>.',
                'This section is used in <b>%s catalogs</b>.',
                catalogs.length), [catalogs.length])}} />
            <ExtendLink extend={showCatalogs} onClick={toggleCatalogs} />
          </p>
          {
            showCatalogs && catalogs.map((catalog, index) => (
              <p key={index}>
                <code className="code-questions">{catalog.uri}</code>
              </p>
            ))
          }
        </>
      }
    </div>
  )
}

SectionInfo.propTypes = {
  section: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired
}

export default SectionInfo
