import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Number from '../forms/Number'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import ElementHeading from '../common/ElementHeading'

const OptionSet = ({ config, optionset, warnings, errors, providers, updateOptionSet, storeOptionSet }) => {
  return (
    <div className="panel panel-default">
      <ElementHeading verboseName={gettext('Option set')} element={optionset} onSave={storeOptionSet} />

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={optionset} field="uri_prefix"
                       warnings={warnings} errors={errors} onChange={updateOptionSet} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={optionset} field="key"
                  warnings={warnings} errors={errors} onChange={updateOptionSet} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={optionset} field="comment"
                      warnings={warnings} errors={errors} rows={4} onChange={updateOptionSet} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={optionset} field="locked"
                      warnings={warnings} errors={errors} onChange={updateOptionSet} />
          </div>
          <div className="col-sm-6">
            <Number config={config} element={optionset} field="order"
                    warnings={warnings} errors={errors} onChange={updateOptionSet} />
          </div>
          <div className="col-sm-12">
            <Select config={config} element={optionset} field="provider_key"
                    warnings={warnings} errors={errors} options={providers} onChange={updateOptionSet} />
          </div>
        </div>
      </div>
    </div>
  )
}

OptionSet.propTypes = {
  config: PropTypes.object.isRequired,
  optionset: PropTypes.object.isRequired,
  warnings: PropTypes.object,
  errors: PropTypes.object,
  providers: PropTypes.array,
  updateOptionSet: PropTypes.func.isRequired,
  storeOptionSet: PropTypes.func.isRequired
}

export default OptionSet
