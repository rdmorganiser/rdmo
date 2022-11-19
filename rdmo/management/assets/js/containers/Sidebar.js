import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import * as configActions from '../actions/configActions'
import * as elementActions from '../actions/elementActions'

import Link from '../components/Link'

class Sidebar extends Component {

  constructor(props) {
    super(props)
  }

  render() {
    const { config, elements, configActions, elementActions } = this.props

    return (
      <div>
        <p>
          <code>{config.resource}</code>
        </p>
        <ul className="list-unstyled">
          <li>
            <Link onClick={configActions.updateConfigAndLocation} resource="catalogs">Catalogs</Link>
          </li>
          <li>
            <Link onClick={configActions.updateConfigAndLocation} resource="sections">Sections</Link>
          </li>
          <li>
            <Link onClick={configActions.updateConfigAndLocation} resource="pages">Pages</Link>
          </li>
          <li>
            <Link onClick={configActions.updateConfigAndLocation} resource="questionsets">Questionsets</Link>
          </li>
          <li>
            <Link onClick={configActions.updateConfigAndLocation} resource="questions">Questions</Link>
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
