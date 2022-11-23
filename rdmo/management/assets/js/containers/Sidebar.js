import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import Link from 'rdmo/core/assets/js/components/Link'

import * as configActions from '../actions/configActions'
import * as elementActions from '../actions/elementActions'


class Sidebar extends Component {

  constructor(props) {
    super(props)
  }

  render() {
    const { config, elements, configActions, elementActions } = this.props

    return (
      <div>
        <ul className="list-unstyled">
          <li>
            <Link onClick={configActions.updateConfigAndLocation} resourceType="catalogs">Catalogs</Link>
          </li>
          <li>
            <Link onClick={configActions.updateConfigAndLocation} resourceType="sections">Sections</Link>
          </li>
          <li>
            <Link onClick={configActions.updateConfigAndLocation} resourceType="pages">Pages</Link>
          </li>
          <li>
            <Link onClick={configActions.updateConfigAndLocation} resourceType="questionsets">Questionsets</Link>
          </li>
          <li>
            <Link onClick={configActions.updateConfigAndLocation} resourceType="questions">Questions</Link>
          </li>
        </ul>
      </div>
    )
  }
}

Sidebar.propTypes = {
  config: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

function mapStateToProps(state, props) {
  return {
    config: state.config,
    elements: state.elements
  }
}

function mapDispatchToProps(dispatch) {
  return {
    configActions: bindActionCreators(configActions, dispatch),
    elementActions: bindActionCreators(elementActions, dispatch)
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Sidebar)
