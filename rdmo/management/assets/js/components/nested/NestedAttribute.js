import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix } from '../common/Filter'
import { BackButton } from '../common/Buttons'

import Attribute from '../element/Attribute'

const NestedAttribute = ({ config, attribute, configActions, elementActions }) => {

  const updateFilterString = (uri) => configActions.updateConfig('filter.attribute.search', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.attribute.uri_prefix', uriPrefix)

  return (
    <>
      <div className="panel panel-default panel-nested">
        <div className="panel-heading">
          <div className="pull-right">
            <BackButton />
          </div>
          <Attribute config={config} attribute={attribute}
                     configActions={configActions} elementActions={elementActions} display="plain" />
        </div>

        <div className="panel-body">
          <div className="row">
            <div className="col-sm-8">
              <FilterString value={get(config, 'filter.attribute.search', '')} onChange={updateFilterString}
                            placeholder={gettext('Filter attributes')} />
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
          <Attribute key={index} config={config} attribute={attribute}
                     configActions={configActions} elementActions={elementActions}
                     display="nested" filter="attribute" indent={1} />
        ))
      }
    </>
  )
}

NestedAttribute.propTypes = {
  config: PropTypes.object.isRequired,
  attribute: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default NestedAttribute
