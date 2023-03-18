import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Number from '../forms/Number'
import OrderedMultiSelect from '../forms/OrderedMultiSelect'
import Select from '../forms/Select'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import ElementButtons from '../common/ElementButtons'

const EditOptionSet = ({ config, optionset, options, providers, updateElement, storeElement }) => {

  const updateOptionSet = (key, value) => updateElement(optionset, key, value)
  const storeOptionSet = () => storeElement('optionsets', optionset)

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons onSave={storeOptionSet} />
        {
          optionset.id ? <div>
            <strong>{gettext('Option set')}{': '}</strong>
            <code className="code-options">{optionset.uri}</code>
          </div> : <strong>{gettext('Create option set')}</strong>
        }
      </div>

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={optionset} field="uri_prefix"
                       onChange={updateOptionSet} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={optionset} field="uri_path"
                  onChange={updateOptionSet} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={optionset} field="comment"
                      rows={4} onChange={updateOptionSet} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={optionset} field="locked"
                      onChange={updateOptionSet} />
          </div>
          <div className="col-sm-6">
            <Number config={config} element={optionset} field="order"
                    onChange={updateOptionSet} />
          </div>
          <div className="col-sm-12">
            <OrderedMultiSelect config={config} element={optionset} field="options"
                                options={options} verboseName="option"
                                onChange={updateOptionSet} />
          </div>
          <div className="col-sm-12">
            <Select config={config} element={optionset} field="provider_key"
                    options={providers} onChange={updateOptionSet} />
          </div>
        </div>
      </div>
    </div>
  )
}

EditOptionSet.propTypes = {
  config: PropTypes.object.isRequired,
  optionset: PropTypes.object.isRequired,
  options: PropTypes.array,
  providers: PropTypes.array,
  storeElement: PropTypes.func.isRequired,
  updateElement: PropTypes.func.isRequired
}

export default EditOptionSet
