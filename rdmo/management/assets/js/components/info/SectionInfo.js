import React from 'react'
import PropTypes from 'prop-types'

import { ExtendLink, CodeLink } from '../common/Links'

import useBool from '../../hooks/useBool'

const SectionInfo = ({ section, elements, elementActions }) => {

  const [showCatalogs, toggleCatalogs] = useBool(false)

  const catalogs = elements.catalogs.filter(e => section.catalogs.includes(e.id))

  const fetchCatalog = (catalog) => elementActions.fetchElement('catalogs', catalog.id)

  return (
    <div className="element-info">
      <p>
        <span dangerouslySetInnerHTML={{
          __html: interpolate(ngettext(
            'This section is used in <b>one catalog</b>.',
            'This section is used in <b>%s catalogs</b>.',
            catalogs.length), [catalogs.length])}} />
        {catalogs.length > 0 && <ExtendLink extend={showCatalogs} onClick={toggleCatalogs} />}
      </p>
      {
        showCatalogs && catalogs.map((catalog, index) => (
          <p key={index}>
            <CodeLink className="code-questions" uri={catalog.uri} onClick={() => fetchCatalog(catalog)} />
          </p>
        ))
      }
    </div>
  )
}

SectionInfo.propTypes = {
  section: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default SectionInfo
