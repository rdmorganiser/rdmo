import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import Breadcrump from '../components/Breadcrump'

import * as configActions from '../actions/configActions'
import * as pageActions from '../actions/pageActions'

// eslint-disable-next-line no-unused-vars
const Main = ({ config, page, configActions, pageActions }) => {
  if (page.display) {
    return (
      <div>
        <Breadcrump project={{}} page={page.page} onJump={(pageId) => pageActions.jump(pageId)} />
        <h2>
            {page.page.title}
        </h2>
      </div>
    )
  }

  // fetching the data is not complete yet, or no action was invoked yet
  return null
}

Main.propTypes = {
  config: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  pageActions: PropTypes.object.isRequired
}

function mapStateToProps(state) {
  return {
    config: state.config,
    page: state.page
  }
}

function mapDispatchToProps(dispatch) {
  return {
    configActions: bindActionCreators(configActions, dispatch),
    pageActions: bindActionCreators(pageActions, dispatch)
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Main)
