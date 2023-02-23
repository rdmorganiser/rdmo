import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import Link from 'rdmo/core/assets/js/components/Link'

import * as configActions from '../actions/configActions'
import * as elementActions from '../actions/elementActions'

import FilterUri from '../components/FilterUri'
import FilterUriPrefix from '../components/FilterUriPrefix'

class Sidebar extends Component {

  constructor(props) {
    super(props)
  }

  getUriPrefixes() {
    const { elements } = this.props

    if (elements.elementType) {
      return elements[elements.elementType].reduce((acc, cur) => {
        if (!acc.includes(cur.uri_prefix)) {
          acc.push(cur.uri_prefix)
        }
        return acc
      }, [])
    } else {
      return []
    }
  }

  render() {
    const { config, elements, configActions, elementActions } = this.props

    return (
      <div>
        <h2>Filter attributes</h2>

        <FilterUri value={config.filterUri} onChange={filterUri => configActions.updateConfig({ filterUri })} />
        <FilterUriPrefix options={this.getUriPrefixes()} value={config.filterUriPrefix}
                         onChange={filterUriPrefix => configActions.updateConfig({ filterUriPrefix })} />

        <h2>Navigation</h2>

        <ul className="list-unstyled">
          <li>
            <Link onClick={() => elementActions.fetchElements('catalogs')}>Catalogs</Link>
          </li>
          <li>
            <Link onClick={() => elementActions.fetchElements('sections')}>Sections</Link>
          </li>
          <li>
            <Link onClick={() => elementActions.fetchElements('pages')}>Pages</Link>
          </li>
          <li>
            <Link onClick={() => elementActions.fetchElements('questionsets')}>Question sets</Link>
          </li>
          <li>
            <Link onClick={() => elementActions.fetchElements('questions')}>Questions</Link>
          </li>
        </ul>

        <ul className="list-unstyled">
          <li>
            <Link onClick={() => elementActions.fetchElements('attributes')}>Attributes</Link>
          </li>
        </ul>

        <ul className="list-unstyled">
          <li>
            <Link onClick={() => elementActions.fetchElements('optionsets')}>Option sets</Link>
          </li>
          <li>
            <Link onClick={() => elementActions.fetchElements('options')}>Options</Link>
          </li>
        </ul>

        <ul className="list-unstyled">
          <li>
            <Link onClick={() => elementActions.fetchElements('conditions')}>Conditions</Link>
          </li>
        </ul>

        <ul className="list-unstyled">
          <li>
            <Link onClick={() => elementActions.fetchElements('tasks')}>Tasks</Link>
          </li>
        </ul>

        <ul className="list-unstyled">
          <li>
            <Link onClick={() => elementActions.fetchElements('views')}>Views</Link>
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