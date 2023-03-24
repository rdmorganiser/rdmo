import React, { Component } from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

import { getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import Page from '../element/Page'
import QuestionSet from '../element/QuestionSet'
import Question from '../element/Question'
import { BackButton } from '../common/ElementButtons'

const NestedPage = ({ config, page, configActions, elementActions }) => {

  const updateFilterUri = (uri) => configActions.updateConfig('filter.page.uri', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.page.uriPrefix', uriPrefix)

  return (
    <>
      <div className="panel panel-default panel-nested">
        <div className="panel-heading">
          <div className="pull-right">
            <BackButton />
          </div>
          <Page config={config} page={page}
                elementActions={elementActions} display="plain" />
        </div>

        <div className="panel-body">
          <div className="row">
            <div className="col-sm-8">
              <FilterUri value={config.filter.page.uri} onChange={updateFilterUri}
                         placeholder={gettext('Filter pages by URI')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix value={config.filter.page.uriPrefix} onChange={updateFilterUriPrefix}
                               options={getUriPrefixes(page.elements)} />
            </div>
          </div>
        </div>
      </div>

      {
        page.elements.map((element, index) => {
          if (isUndefined(element.text)) {
            return <QuestionSet key={index} config={config} questionset={element} elementActions={elementActions}
                                display="nested" filter={config.filter.page} indent={1} />
          } else {
            return <Question key={index} config={config} question={element} elementActions={elementActions}
                             display="nested" filter={config.filter.page} indent={1} />
          }
        })
      }
    </>
  )
}

NestedPage.propTypes = {
  config: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default NestedPage
