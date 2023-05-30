import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import isEmpty from 'lodash/isEmpty'

import * as elementActions from '../actions/elementActions'
import * as importActions from '../actions/importActions'

import ElementsSidebar from '../components/sidebar/ElementsSidebar'
import ImportSidebar from '../components/sidebar/ImportSidebar'

const Sidebar = ({ config, elements, imports, elementActions, importActions }) => {
  if (isEmpty(imports.elements)) {
    return <ElementsSidebar config={config} elements={elements}
                            elementActions={elementActions} importActions={importActions} />
  } else {
    return <ImportSidebar config={config} imports={imports} importActions={importActions} />
  }
}

Sidebar.propTypes = {
  config: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  imports: PropTypes.object.isRequired,
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
    elementActions: bindActionCreators(elementActions, dispatch),
    importActions: bindActionCreators(importActions, dispatch)
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Sidebar)
