import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import isEmpty from 'lodash/isEmpty'

import Link from 'rdmo/core/assets/js/components/Link'
import UploadForm from '../components/forms/UploadForm'

import * as configActions from '../actions/configActions'
import * as elementActions from '../actions/elementActions'
import * as importActions from '../actions/importActions'

import ElementsSidebar from '../components/sidebar/ElementsSidebar'
import ImportSidebar from '../components/sidebar/ImportSidebar'

class Sidebar extends Component {

  constructor(props) {
    super(props)
  }

  render() {
    const { config, imports, configActions, elementActions, importActions } = this.props

    if (isEmpty(imports.elements)) {
      return <ElementsSidebar config={config} elementActions={elementActions} importActions={importActions} />
    } else {
      return <ImportSidebar config={config} imports={imports} importActions={importActions} />
    }
  }
}

Sidebar.propTypes = {
  config: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  imports: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  importActions: PropTypes.object.isRequired
}

function mapStateToProps(state, props) {
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

export default connect(mapStateToProps, mapDispatchToProps)(Sidebar)
