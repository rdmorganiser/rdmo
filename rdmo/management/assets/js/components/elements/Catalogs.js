import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Catalog from '../element/Catalog'
import { BackButton, NewButton } from '../common/ElementButtons'

const Catalogs = ({ config, catalogs, elementActions }) => {

  const createCatalog = () => elementActions.createElement('catalogs')

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <NewButton onClick={createCatalog} />
        </div>
        <strong>{gettext('Catalogs')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, catalogs).map((catalog, index) => (
          <Catalog key={index} config={config} catalog={catalog}
                   elementActions={elementActions} />
        ))
      }
      </ul>
    </div>
  )
}

Catalogs.propTypes = {
  config: PropTypes.object.isRequired,
  catalogs: PropTypes.array.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Catalogs
