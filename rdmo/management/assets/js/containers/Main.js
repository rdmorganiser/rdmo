import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import get from 'lodash/get'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'

import * as configActions from '../actions/configActions'
import * as elementActions from '../actions/elementActions'
import * as importActions from '../actions/importActions'

import { MainErrors } from '../components/common/Errors'

import Edit from '../components/main/Edit'
import Elements from '../components/main/Elements'
import Import from '../components/main/Import'
import Nested from '../components/main/Nested'

const Main = ({ config, elements, imports, configActions, elementActions, importActions }) => {
  const { element, elementType, elementId, elementAction } = elements

  // check if anything was loaded yet
  if (isNil(elementType)) {
    return null
  }

  // check if an error occurred
  if (!isNil(elements.errors.api)) {
    return <MainErrors errors={elements.errors.api} />
  } else if (get(elements, 'element.errors.api')) {
    return <MainErrors errors={get(elements, 'element.errors.api')} />
  } else if (!isNil(imports.errors.file)) {
    return <MainErrors errors={imports.errors.file} />
  }

  if (!isEmpty(imports.elements)) {
    return <Import config={config} imports={imports}
                   configActions={configActions} importActions={importActions} />
  }

  // check if the nested components should be displayed
  if (!isNil(element) && elementAction === 'nested') {
    return <Nested config={config} elements={elements}
                   configActions={configActions} elementActions={elementActions} />
  }

  // check if the edit components should be displayed
  if (!isNil(element)) {
    return <Edit config={config} elements={elements}
                 configActions={configActions} elementActions={elementActions} />
  }

  // check if the list components should be displayed
  if (isNil(elementId) && isNil(elementAction)) {
    return <Elements config={config} elements={elements}
                     configActions={configActions} elementActions={elementActions} />
  }

  // fetching the data is not complete yet, or no action was invoked yet
  return null
}

Main.propTypes = {
  config: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  imports: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

function mapStateToProps(state) {
  return {
    config: state.config,
    elements: state.elements,
    imports: state.imports
  }
}

function mapDispatchToProps(dispatch) {
  return {
    configActions: bindActionCreators(configActions, dispatch),
    elementActions: bindActionCreators(elementActions, dispatch),
    importActions: bindActionCreators(importActions, dispatch)
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Main)
