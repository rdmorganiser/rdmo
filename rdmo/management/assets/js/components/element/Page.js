import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

import ElementHeading from '../common/ElementHeading'

const Page = ({ config, page, warnings, errors, updatePage, storePage }) => {
  return (
    <div className="panel panel-default">
      <ElementHeading verboseName={gettext('Page')} element={page} onSave={storePage} />

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={page} field="uri_prefix"
                  warnings={warnings} errors={errors} onChange={updatePage} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={page} field="key"
                  warnings={warnings} errors={errors} onChange={updatePage} />
          </div>
          <div className="col-sm-12">
            <Textarea config={config} element={page} field="comment"
                      warnings={warnings} errors={errors} rows={4} onChange={updatePage} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={page} field="locked"
                      warnings={warnings} errors={errors} onChange={updatePage} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={page} field="is_collection"
                      warnings={warnings} errors={errors} onChange={updatePage} />
          </div>
          <div className="col-sm-12">
            <Tabs id="#catalog-tabs" defaultActiveKey={0} animation={false}>
              {
                config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                  const classNames = ''
                  return (
                    <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                      <div className="row">
                        <div className="col-sm-12">
                          <Text config={config} element={page}
                                field={`title_${lang_code }`} warnings={warnings} errors={errors}
                                onChange={updatePage} />
                        </div>
                        <div className="col-sm-12">
                          <Textarea config={config} element={page}
                                    field={`help_${lang_code }`} warnings={warnings} errors={errors}
                                    rows={4} onChange={updatePage} />
                        </div>
                        <div className="col-sm-6">
                          <Text config={config} element={page}
                                field={`verbose_name_${lang_code }`} warnings={warnings} errors={errors}
                                onChange={updatePage} />
                        </div>
                        <div className="col-sm-6">
                          <Text config={config} element={page}
                                field={`verbose_name_plural_${lang_code }`} warnings={warnings} errors={errors}
                                onChange={updatePage} />
                        </div>
                      </div>
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

Page.propTypes = {
  config: PropTypes.object.isRequired,
  catalog: PropTypes.object.isRequired,
  warnings: PropTypes.object,
  errors: PropTypes.object,
  updatePage: PropTypes.func.isRequired,
  storePage: PropTypes.func.isRequired
}

export default Page