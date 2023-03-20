import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Section from '../element/Section'
import Page from '../element/Page'
import { BackButton } from '../common/ElementButtons'

const NestedCatalog = ({ config, section, elementActions }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
        </div>
        <Section config={config} section={section}
                 elementActions={elementActions} list={false} />
      </div>

      <ul className="list-group">
      {
        filterElements(config, section.elements).map((page, index) => (
          <Page key={index} config={config} page={page}
                elementActions={elementActions} />
        ))
      }
      </ul>
    </div>
  )
}

NestedCatalog.propTypes = {
  config: PropTypes.object.isRequired,
  section: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default NestedCatalog
