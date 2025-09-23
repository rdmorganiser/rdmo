import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import { get } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix } from '../common/Filter'
import { BackButton } from '../common/Buttons'

import Attribute from '../element/Attribute'

const NestedAttribute = ({ attribute }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const updateFilterString = (uri) => dispatch(updateConfig('filter.attribute.search', uri))
  const updateFilterUriPrefix = (uriPrefix) => dispatch(updateConfig('filter.attribute.uri_prefix', uriPrefix))

  return (
    <>
      <div className="panel panel-default panel-nested">
        <div className="panel-heading">
          <div className="pull-right">
            <BackButton />
          </div>
          <Attribute attribute={attribute} display="plain" />
        </div>

        <div className="panel-body">
          <div className="row">
            <div className="col-sm-8">
              <FilterString value={get(config, 'filter.attribute.search', '')} onChange={updateFilterString}
                            label={gettext('Filter attributes')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix value={get(config, 'filter.attribute.uri_prefix', '')} onChange={updateFilterUriPrefix}
                               options={getUriPrefixes(attribute.elements)} />
            </div>
          </div>
        </div>
      </div>

      {
        attribute.elements.map((attribute, index) => (
          <Attribute key={index} attribute={attribute} display="nested" filter="attribute" indent={1} />
        ))
      }
    </>
  )
}

NestedAttribute.propTypes = {
  attribute: PropTypes.object.isRequired
}

export default NestedAttribute
