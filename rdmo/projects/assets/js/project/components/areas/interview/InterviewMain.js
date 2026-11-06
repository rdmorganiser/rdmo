import React from 'react'
import { useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'

import Contact from './main/Contact'
import Page from './main/page/Page'
import BackLink from './sidebar/BackLink'
import ManagementButton from './sidebar/ManagementButton'
import Navigation from './sidebar/Navigation'
import Progress from './sidebar/Progress'

const InterviewMain = () => {
  const { page } = useSelector((state) => state.interview)

  return page && (
    <div className="project-interview-main">
      <h1 className="mb-5">
        <Html html={page.title} />
      </h1>
      <div className="row">
        <div className="col-md-9">
          <Page />
        </div>
        <div className="col-md-3">
          <Navigation />
          <Progress />
          <ManagementButton />
          <BackLink />
        </div>
      </div>

      <Contact />
    </div>
  )
}

export default InterviewMain
