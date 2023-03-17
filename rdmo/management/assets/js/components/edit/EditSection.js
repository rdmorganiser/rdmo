import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import OrderedMultiSelect from '../forms/OrderedMultiSelect'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import Select from '../forms/Select'
import UriPrefix from '../forms/UriPrefix'

import ElementButtons from '../common/ElementButtons'

const EditSection = ({ config, section, pages, updateElement, storeElement }) => {

  const updateSection = (key, value) => updateElement(section, key, value)
  const storeSection = () => storeElement('sections', section)

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons onSave={storeSection} />
        <strong>{gettext('Section')}{': '}</strong>
        <code className="code-questions">{section.uri}</code>
      </div>

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={section} field="uri_prefix"
                       onChange={updateSection} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={section} field="uri_path"
                  onChange={updateSection} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={section} field="comment"
                      rows={4} onChange={updateSection} />
          </div>
          <div className="col-sm-12">
            <Checkbox config={config} element={section} field="locked"
                      onChange={updateSection} />
          </div>
          <div className="col-sm-12">
            <OrderedMultiSelect config={config} element={section} field="pages"
                                options={pages} verboseName="page"
                                onChange={updateSection} />
          </div>
          <div className="col-sm-12">
            <Tabs id="#section-tabs" defaultActiveKey={0} animation={false}>
              {
                config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                  const classNames = ''
                  return (
                    <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                      <Text config={config} element={section} field={`title_${lang_code }`}
                            onChange={updateSection} />
                    </Tab>
                  )
                })
              }
            </Tabs>
          </div>
        </div>
      </div>
    </div>
  )
}

EditSection.propTypes = {
  config: PropTypes.object.isRequired,
  section: PropTypes.object.isRequired,
  pages: PropTypes.array,
  storeElement: PropTypes.func.isRequired,
  updateElement: PropTypes.func.isRequired
}

export default EditSection
