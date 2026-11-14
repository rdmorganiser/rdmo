import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { isEmpty } from 'lodash'

import { useConfig } from 'rdmo/core/assets/js/hooks'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { BackButton, NewButton } from '../common/Buttons'
import { FilterSite, FilterString, FilterUriPrefix } from '../common/Filter'
import Attribute from '../element/Attribute'

const Attributes = () => {
  const dispatch = useDispatch()

  const settings = useSelector((state) => state.settings)
  const sites = useSelector((state) => state.sites)
  const attributes = useSelector((state) => state.elements.attributes)

  const [filterString, setFilterString] = useConfig('filter.attributes.search', '')
  const [filterUriPrefix, setFilterUriPrefix] = useConfig('filter.attributes.uri_prefix', '')
  const [filterEditor, setFilterEditor] = useConfig('filter.editors', '')

  const createAttribute = () => dispatch(createElement('attributes'))

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex flex-column flex-sm-row align-items-sm-center gap-2">
          <strong className="flex-grow-1 text-center text-sm-start">{gettext('Attributes')}</strong>
          <BackButton />
          <NewButton onClick={createAttribute} />
        </div>
      </div>

      <div className="card-body pb-0">
        <div className="mb-lg-2">
          <div className="row">
            <div className={settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
              <FilterString
                value={filterString} onChange={setFilterString}
                label={gettext('Filter attributes')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix
                value={filterUriPrefix} onChange={setFilterUriPrefix}
                options={getUriPrefixes(attributes)} />
            </div>
            {
              settings.multisite && (
                <div className="col-sm-2">
                  <FilterSite
                    value={filterEditor} onChange={setFilterEditor}
                    options={sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
                </div>
              )
            }
          </div>
        </div>
      </div>

      {
        !isEmpty(attributes) && (
          <ul className="list-group list-group-flush border-top">
            {
              attributes.map((attribute, index) => (
                <Attribute
                  key={index} attribute={attribute}
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
