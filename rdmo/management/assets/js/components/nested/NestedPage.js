import React, { Component } from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

import { filterElements } from '../../utils/filter'

import Page from '../element/Page'
import QuestionSet from '../element/QuestionSet'
import Question from '../element/Question'
import ElementButtons from '../common/ElementButtons'

const NestedPage = ({ config, page, fetchElement, storeElement }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons />
        <Page config={config} page={page}
              fetchElement={fetchElement} storeElement={storeElement} list={false} />
      </div>

      <ul className="list-group">
        {
          filterElements(config, page.elements).map((element, index) => {
            if (isUndefined(element.text)) {
              return <QuestionSet key={index} config={config} questionset={element}
                                  fetchElement={fetchElement} storeElement={storeElement} />
            } else {
              return <Question key={index} config={config} question={element}
                               fetchElement={fetchElement} storeElement={storeElement} />
            }
          })
        }
      </ul>
    </div>
  )
}

NestedPage.propTypes = {
  config: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
  fetchElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default NestedPage
