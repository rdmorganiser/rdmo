import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import ElementHeading from '../common/ElementHeading'

const Condition = ({ config, condition, warnings, errors, updateCondition, storeCondition,
                     relations, attributes, options }) => {
  return (
    <div className="panel panel-default">
      <ElementHeading verboseName={gettext('Condition')} element={condition} onSave={storeCondition} />

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={condition} field="uri_prefix"
                       warnings={warnings} errors={errors} onChange={updateCondition} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={condition} field="key"
                  warnings={warnings} errors={errors} onChange={updateCondition} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={condition} field="comment"
                      warnings={warnings} errors={errors} rows={4} onChange={updateCondition} />
          </div>
          <div className="col-sm-12">
            <Checkbox config={config} element={condition} field="locked"
                      warnings={warnings} errors={errors} onChange={updateCondition} />
          </div>
          <div className="col-sm-6">
            <Select config={config} element={condition} field="source"
                    warnings={warnings} errors={errors} options={attributes} onChange={updateCondition} />
          </div>
          <div className="col-sm-6">
            <Select config={config} element={condition} field="relation"
                    warnings={warnings} errors={errors} options={relations} onChange={updateCondition} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={condition} field="target_text"
                  warnings={warnings} errors={errors} onChange={updateCondition} />
          </div>
          <div className="col-sm-6">
            <Select config={config} element={condition} field="target_option"
                    warnings={warnings} errors={errors} options={options} onChange={updateCondition} />
          </div>
        </div>
      </div>
    </div>
  )
}

Condition.propTypes = {
  config: PropTypes.object.isRequired,
  condition: PropTypes.object.isRequired,
  warnings: PropTypes.object.isRequired,
  errors: PropTypes.object.isRequired,
  updateCondition: PropTypes.func.isRequired,
  storeCondition: PropTypes.func.isRequired,
  relations: PropTypes.array,
  attributes: PropTypes.array,
  options: PropTypes.array
}

export default Condition
