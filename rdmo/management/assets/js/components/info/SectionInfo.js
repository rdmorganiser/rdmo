import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

import { fetchElement } from '../../actions/elementActions'

import { ExtendLink, CodeLink } from '../common/Links'

import useBool from '../../hooks/useBool'

const SectionInfo = ({ section }) => {
  const dispatch = useDispatch()

  const elements = useSelector((state) => state.elements)

  const [showCatalogs, toggleCatalogs] = useBool(false)

  const catalogs = elements.catalogs.filter(e => section.catalogs.includes(e.id))

  const fetchCatalog = (catalog) => dispatch(fetchElement('catalogs', catalog.id))

  return (
    <div className="element-info">
      <p>
        <Html html={interpolate(ngettext(
          'This section is used in <b>one catalog</b>.',
          'This section is used in <b>%s catalogs</b>.',
          catalogs.length), [catalogs.length])} />
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
  section: PropTypes.object.isRequired
}

export default SectionInfo
