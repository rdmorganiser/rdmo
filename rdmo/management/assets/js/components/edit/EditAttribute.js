import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import ElementButtons from '../common/ElementButtons'

const EditAttribute = ({ config, attribute, attributes, updateElement, storeElement }) => {

  const updateAttribute = (key, value) => updateElement(attribute, key, value)
  const storeAttribute = () => storeElement('attributes', attribute)

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons onSave={storeAttribute} />
        <strong>{gettext('Attribute')}{': '}</strong>
        <code className="code-domain">{attribute.uri}</code>
      </div>

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={attribute} field="uri_prefix"
                       onChange={updateAttribute} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={attribute} field="key"
                  onChange={updateAttribute} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={attribute} field="comment"
                      rows={4} onChange={updateAttribute} />
          </div>
          <div className="col-sm-12">
            <Checkbox config={config} element={attribute} field="locked"
                      onChange={updateAttribute} />
          </div>
          <div className="col-sm-12">
            <Select config={config} element={attribute} field="parent"
                    options={attributes} onChange={updateAttribute} />
          </div>
        </div>
      </div>
    </div>
  )
}

EditAttribute.propTypes = {
  config: PropTypes.object.isRequired,
  attribute: PropTypes.object.isRequired,
  attributes: PropTypes.array,
  storeElement: PropTypes.func.isRequired,
  updateElement: PropTypes.func.isRequired
}

export default EditAttribute
