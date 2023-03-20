import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Section from '../element/Section'
import { BackButton, NewButton } from '../common/ElementButtons'

const Sections = ({ config, sections, elementActions }) => {

  const createSection = () => elementActions.createElement('sections')

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <NewButton onClick={createSection} />
        </div>
        <strong>{gettext('Sections')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, sections).map((section, index) => (
          <Section key={index} config={config} section={section}
                   elementActions={elementActions} />
        ))
      }
      </ul>
    </div>
  )
}

Sections.propTypes = {
  config: PropTypes.object.isRequired,
  sections: PropTypes.array.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Sections
