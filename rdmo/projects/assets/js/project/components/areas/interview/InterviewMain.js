import React from 'react'

import Page from './main/page/Page'
import Navigation from './sidebar/Navigation'

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
        </div>
      </div>
    </div>
  )
}

export default InterviewMain
