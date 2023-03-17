import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Catalog from '../element/Catalog'
import ElementButtons from '../common/ElementButtons'

const Catalogs = ({ config, catalogs, fetchElement, storeElement }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons />
        <strong>{gettext('Catalogs')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, catalogs).map((catalog, index) => (
          <Catalog key={index} config={config} catalog={catalog}
                   fetchElement={fetchElement} storeElement={storeElement} />
        ))
      }
      </ul>
    </div>
  )
}

Catalogs.propTypes = {
  config: PropTypes.object.isRequired,
  catalogs: PropTypes.array.isRequired,
  fetchElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default Catalogs
