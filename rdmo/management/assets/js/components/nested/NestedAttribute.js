import React from 'react'
import PropTypes from 'prop-types'

import { useConfig } from 'rdmo/core/assets/js/hooks'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix } from '../common/Filter'
import Attribute from '../element/Attribute'

const NestedAttribute = ({ attribute }) => {
  const [filterString, setFilterString] = useConfig('filter.attribute.search', '')
  const [filterUriPrefix, setFilterUriPrefix] = useConfig('filter.attribute.uri_prefix', '')


  return (
    <>
      <div className="card">
        <div className="card-header">
          <Attribute attribute={attribute} display="plain" backButton={true} />
        </div>

        <div className="card-body pb-0">
          <div className="mb-lg-2">
            <div className="row">
              <div className="col-sm-8">
                <FilterString
                  value={filterString} onChange={setFilterString}
                  label={gettext('Filter attributes')} />
              </div>
              <div className="col-sm-4">
                <FilterUriPrefix
                  value={filterUriPrefix} onChange={setFilterUriPrefix}
                  options={getUriPrefixes(attribute.elements)} />
              </div>
            </div>
          </div>
        </div>

        <div className="card-body border-top pt-0">
          {
            attribute.elements.map((attribute, index) => (
              <Attribute key={index} attribute={attribute} display="nested" filter="attribute" indent={1} />
            ))
          }
        </div>
      </div>
    </>
  )
}

NestedAttribute.propTypes = {
  attribute: PropTypes.object.isRequired
}

export default NestedAttribute
