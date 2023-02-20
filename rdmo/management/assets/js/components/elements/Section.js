import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import Checkbox from '../forms/Checkbox'
import Select from '../forms/Select'
import UriPrefix from '../forms/UriPrefix'

const Section = ({ config, section, warnings, errors, updateSection, storeSection }) => {
  return (
    <div>
      <div className="panel panel-default">
        <div className="panel-heading">
          <div className="pull-right">
            <button className="btn btn-xs btn-default" onClick={event => history.back()}>
              {gettext('Back')}
            </button>
            {' '}
            <button className="btn btn-xs btn-primary" onClick={event => storeSection()}>
              {gettext('Save')}
            </button>
          </div>
          <div>
            <strong>{gettext('Section')}</strong>
          </div>
        </div>
        <div className="panel-body">
          <code className="code-questions">{section.uri}</code>
        </div>
      </div>

      <div className="row">
        <div className="col-sm-6">
          <UriPrefix config={config} element={section} elementType="sections" field="uri_prefix"
                     warnings={warnings} errors={errors} onChange={updateSection} />
        </div>
        <div className="col-sm-6">
          <Text config={config} element={section} elementType="sections" field="key"
                warnings={warnings} errors={errors} onChange={updateSection} />
        </div>
        <div className="col-sm-12">
          <Textarea config={config} element={section} elementType="sections" field="comment"
                    warnings={warnings} errors={errors} rows={4} onChange={updateSection} />
        </div>
        <div className="col-sm-12">
          <Checkbox config={config} element={section} elementType="sections" field="locked"
                    warnings={warnings} errors={errors} onChange={updateSection} />
        </div>
        <div className="col-sm-12">
          <Tabs id="#section-tabs" defaultActiveKey={0} animation={false}>

            <Tab className="pt-10" eventKey={0} title={gettext('General')}>

            </Tab>

            {
              config.settings && config.settings.languages.map(([lang_code, lang], index) => {
                const classNames = ''
                return (
                  <Tab className="pt-10" key={index} eventKey={index + 1} title={lang}>
                    <Text config={config} element={section} elementType="sections"
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
  )
}

Section.propTypes = {
  config: PropTypes.object.isRequired,
  section: PropTypes.object.isRequired,
  warnings: PropTypes.object,
  errors: PropTypes.object,
  updateSection: PropTypes.func.isRequired,
  storeSection: PropTypes.func.isRequired
}

export default Section
