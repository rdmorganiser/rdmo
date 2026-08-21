import React from 'react'

import Page from './main/page/Page'
import Back from './sidebar/Back'
import Navigation from './sidebar/Navigation'
import Progress from './sidebar/Progress'

const InterviewMain = () => {
  const page = {
    title: 'Lorem ipsum dolor sit amet',
  }

  return (
    <div className="project-interview-main">
      <h2>{page.title}</h2>

      <div className="row">
        <div className="col-md-9">
          <Page />
        </div>
        <div className="col-md-3">
          <Navigation />
          <Progress />
          <Back />
        </div>
      </div>
    </div>
  )
}

export default InterviewMain
