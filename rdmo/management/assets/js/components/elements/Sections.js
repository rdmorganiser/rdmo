import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Section from '../element/Section'
import ElementButtons from '../common/ElementButtons'

const Sections = ({ config, sections, fetchElement, storeElement }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons />
        <strong>{gettext('Sections')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, sections).map((section, index) => (
          <Section key={index} config={config} section={section}
                   fetchElement={fetchElement} storeElement={storeElement} />
        ))
      }
      </ul>
    </div>
  )
}

Sections.propTypes = {
  config: PropTypes.object.isRequired,
  sections: PropTypes.array.isRequired,
  fetchElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default Sections
