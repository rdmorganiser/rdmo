import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import ElementButtons from '../common/ElementButtons'

const EditCondition = ({ config, condition, relations, attributes, options,
                         updateElement, storeElement }) => {

  const updateCondition = (key, value) => updateElement(condition, key, value)
  const storeCondition = () => storeElement('conditions', condition)

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons onSave={storeCondition} />
        <strong>{gettext('Condition')}{': '}</strong>
        <code className="code-conditions">{condition.uri}</code>
      </div>

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={condition} field="uri_prefix"
                       onChange={updateCondition} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={condition} field="key"
                  onChange={updateCondition} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={condition} field="comment"
                      rows={4} onChange={updateCondition} />
          </div>
          <div className="col-sm-12">
            <Checkbox config={config} element={condition} field="locked"
                      onChange={updateCondition} />
          </div>
          <div className="col-sm-6">
            <Select config={config} element={condition} field="source"
                    options={attributes} onChange={updateCondition} />
          </div>
          <div className="col-sm-6">
            <Select config={config} element={condition} field="relation"
                    options={relations} onChange={updateCondition} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={condition} field="target_text"
                  onChange={updateCondition} />
          </div>
          <div className="col-sm-6">
            <Select config={config} element={condition} field="target_option"
                    options={options} onChange={updateCondition} />
          </div>
        </div>
      </div>
    </div>
  )
}

EditCondition.propTypes = {
  config: PropTypes.object.isRequired,
  condition: PropTypes.object.isRequired,
  relations: PropTypes.array,
  attributes: PropTypes.array,
  options: PropTypes.array,
  storeElement: PropTypes.func.isRequired,
  updateElement: PropTypes.func.isRequired
}

export default EditCondition
