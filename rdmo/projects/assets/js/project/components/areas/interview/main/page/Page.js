import React from 'react'

const Page = () => {
  const page = {
    // eslint-disable-next-line max-len
    help: 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.'
  }

  return (
    <div className="project-interview-page">
      <div className="project-interview-page-help">
        {page.help}
      </div>
    </div>
  )
}

export default Page
