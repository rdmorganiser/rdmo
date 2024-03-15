import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import Buttons from '../components/Buttons'
import Navigation from '../components/Navigation'
import Overview from '../components/Overview'
import Progress from '../components/Progress'

import * as configActions from '../actions/configActions'
import * as pageActions from '../actions/pageActions'

// eslint-disable-next-line no-unused-vars
const Sidebar = ({ config, page, configActions, pageActions }) => {
  if (page.display) {
    return (
      <div>
        <Overview project={page.project} />
        <Progress progress={page.progress} />
        <Buttons currentPage={page.page} onPrev={() => pageActions.prev()} onNext={() => pageActions.next()} />
        <Navigation currentPage={page.page} navigation={page.navigation}
                    onJump={(sectionId, pageId) => pageActions.jump(sectionId, pageId)} />
      </div>
    )
  }

  // fetching the data is not complete yet, or no action was invoked yet
  return null
}

Sidebar.propTypes = {
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

export default connect(mapStateToProps, mapDispatchToProps)(Sidebar)
