import React from 'react'
import { useSelector } from 'react-redux'
import { isEmpty } from 'lodash'

const Pending = () => {
  const pending = useSelector((state) => state.pending)

  console.log(pending)

  return (
    !isEmpty(pending.items) && (
      <i className="fa fa-circle-o-notch fa-spin fa-fw" aria-hidden="true"></i>
    )
  )
}

export default Pending
