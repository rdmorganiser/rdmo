import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite } from '../common/Filter'
import { BackButton, NewButton } from '../common/Buttons'

import Attribute from '../element/Attribute'

const Attributes = ({ config, attributes, configActions, elementActions }) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.attributes.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.attributes.uri_prefix', value)
  const updateFilterEditor = (value) => configActions.updateConfig('filter.editors', value)
  const createAttribute = () => elementActions.createElement('attributes')

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <NewButton onClick={createAttribute} />
        </div>
        <strong>{gettext('Attributes')}</strong>
      </div>

      <div className="panel-body">
        <div className="row">
          <div className={config.settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
            <FilterString value={get(config, 'filter.attributes.search', '')} onChange={updateFilterString}
                          label={gettext('Filter attributes')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={get(config, 'filter.attributes.uri_prefix', '')} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(attributes)} />
          </div>
          {
            config.settings.multisite && <div className="col-sm-2">
              <FilterSite value={get(config, 'filter.editors', '')} onChange={updateFilterEditor}
                          options={config.sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
            </div>
          }
        </div>
      </div>

      <ul className="list-group">
      {
        attributes.map((attribute, index) => (
          <Attribute key={index} config={config} attribute={attribute}
                     configActions={configActions} elementActions={elementActions}
                     filter="attributes" filterEditors={true} />
        ))
      }
      </ul>
    </div>
  )
}

Attributes.propTypes = {
  config: PropTypes.object.isRequired,
  attributes: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Attributes
