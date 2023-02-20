import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap';

import Checkbox from '../forms/Checkbox'
import Text from '../forms/Text'
import Textarea from '../forms/Textarea'
import UriPrefix from '../forms/UriPrefix'

const Page = ({ config, page, warnings, errors, updatePage, storePage }) => {
  return (
    <div>
      <div className="panel panel-default">
        <div className="panel-heading">
          <div className="pull-right">
            <button className="btn btn-xs btn-default" onClick={event => history.back()}>
              {gettext('Back')}
            </button>
            {' '}
            <button className="btn btn-xs btn-primary" onClick={event => storePage()}>
              {gettext('Save')}
            </button>
          </div>
          <div>
            <strong>{gettext('Page')}</strong>
          </div>
        </div>
        <div className="panel-body">
          <code className="code-questions">{page.uri}</code>
        </div>
      </div>

      <div className="row">
        <div className="col-sm-6">
          <UriPrefix config={config} element={page} elementType="catalogs" field="uri_prefix"
                warnings={warnings} errors={errors} onChange={updatePage} />
        </div>
        <div className="col-sm-6">
          <Text config={config} element={page} elementType="catalogs" field="key"
                warnings={warnings} errors={errors} onChange={updatePage} />
        </div>
        <div className="col-sm-12">
          <Textarea config={config} element={page} elementType="catalogs" field="comment"
                    warnings={warnings} errors={errors} rows={4} onChange={updatePage} />
        </div>
        <div className="col-sm-12">
          <Checkbox config={config} element={page} elementType="catalogs" field="locked"
                    warnings={warnings} errors={errors} onChange={updatePage} />
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
