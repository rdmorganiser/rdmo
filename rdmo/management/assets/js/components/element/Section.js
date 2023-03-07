import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import OrderedMultiSelect from '../forms/OrderedMultiSelect'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import Select from '../forms/Select'
import UriPrefix from '../forms/UriPrefix'

import ElementHeading from '../common/ElementHeading'

const Section = ({ config, section, warnings, errors, updateSection, storeSection,
                   pages }) => {
  return (
    <div className="panel panel-default">
      <ElementHeading verboseName={gettext('Section')} element={section} onSave={storeSection} />

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={section} field="uri_prefix"
                       warnings={warnings} errors={errors} onChange={updateSection} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={section} field="key"
                  warnings={warnings} errors={errors} onChange={updateSection} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={section} field="comment"
                      warnings={warnings} errors={errors} rows={4} onChange={updateSection} />
          </div>
          <div className="col-sm-12">
            <Checkbox config={config} element={section} field="locked"
                      warnings={warnings} errors={errors} onChange={updateSection} />
          </div>
          <div className="col-sm-12">
            <OrderedMultiSelect config={config} element={section} field="pages"
                                warnings={warnings} errors={errors}
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
                      <Text config={config} element={section}
                            field={`title_${lang_code }`} warnings={warnings} errors={errors}
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

Section.propTypes = {
  config: PropTypes.object.isRequired,
  section: PropTypes.object.isRequired,
  warnings: PropTypes.object.isRequired,
  errors: PropTypes.object.isRequired,
  updateSection: PropTypes.func.isRequired,
  storeSection: PropTypes.func.isRequired,
  pages: PropTypes.array
}

export default Section
