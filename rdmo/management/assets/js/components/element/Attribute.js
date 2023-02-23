import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import ElementHeading from '../common/ElementHeading'

const Attribute = ({ config, attribute, warnings, errors, attributes, updateAttribute, storeAttribute }) => {
  return (
    <div className="panel panel-default">
      <ElementHeading verboseName={gettext('Attribute')} element={attribute} onSave={storeAttribute} />

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={attribute} field="uri_prefix"
                  warnings={warnings} errors={errors} onChange={updateAttribute} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={attribute} field="key"
                  warnings={warnings} errors={errors} onChange={updateAttribute} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={attribute} field="comment"
                      warnings={warnings} errors={errors} rows={4} onChange={updateAttribute} />
          </div>
          <div className="col-sm-12">
            <Checkbox config={config} element={attribute} field="locked"
                      warnings={warnings} errors={errors} onChange={updateAttribute} />
          </div>
          <div className="col-sm-12">
            <Select config={config} element={attribute} field="parent"
                    warnings={warnings} errors={errors} options={attributes} onChange={updateAttribute} />
          </div>
        </div>
      </div>
    </div>
  )
}

Attribute.propTypes = {
  config: PropTypes.object.isRequired,
  attribute: PropTypes.object.isRequired,
  warnings: PropTypes.object,
  errors: PropTypes.object,
  attributes: PropTypes.array,
  updateAttribute: PropTypes.func.isRequired,
  storeAttribute: PropTypes.func.isRequired
}

export default Attribute
