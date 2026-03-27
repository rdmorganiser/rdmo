import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { get, isEmpty } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { BackButton, NewButton } from '../common/Buttons'
import { FilterSite, FilterString, FilterUriPrefix } from '../common/Filter'
import Attribute from '../element/Attribute'

const Attributes = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const attributes = useSelector((state) => state.elements.attributes)

  const updateFilterString = (value) => dispatch(updateConfig('filter.attributes.search', value))
  const updateFilterUriPrefix = (value) => dispatch(updateConfig('filter.attributes.uri_prefix', value))
  const updateFilterEditor = (value) => dispatch(updateConfig('filter.editors', value))
  const createAttribute = () => dispatch(createElement('attributes'))

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex align-items-center gap-2">
          <strong className="me-auto">{gettext('Attributes')}</strong>
          <BackButton />
          <NewButton onClick={createAttribute} />
        </div>
      </div>

      <div className="card-body pb-0">
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
            config.settings.multisite && (
              <div className="col-sm-2">
                <FilterSite value={get(config, 'filter.editors', '')} onChange={updateFilterEditor}
                  options={config.sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
              </div>
            )
          }
        </div>
      </div>

      {
        !isEmpty(attributes) && (
          <ul className="list-group list-group-flush">
            {
              attributes.map((attribute, index) => (
                <Attribute key={index} config={config} attribute={attribute}
                  filter="attributes" filterEditors={true} />
              ))
            }
          </ul>
        )
      }
    </div>
  )
}

export default Attributes
