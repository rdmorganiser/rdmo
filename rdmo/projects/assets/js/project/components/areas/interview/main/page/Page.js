import React, { useEffect } from 'react'
import { useSelector } from 'react-redux'
import { isNil, minBy } from 'lodash'
import get from 'lodash/get'

import Question from '../question/Question'
import QuestionSet from '../questionset/QuestionSet'

import PageButtons from './PageButtons'
import PageHead from './PageHead'
import PageHelp from './PageHelp'
import PageManagement from './PageManagement'

const Page = () => {
  const config = useSelector((state) => state.config)
  const { page, sets, values } = useSelector((state) => state.interview)

  const currentSetPrefix = ''

  let currentSetIndex = page.is_collection ? get(config, 'page.currentSetIndex', 0) : 0

  let currentSet = sets.find((set) => (
    (set.set_prefix == currentSetPrefix) &&
    (set.set_index == currentSetIndex) &&
    (set.element == page)
  ))

  // sanity check
  if (isNil(currentSet)) {
    currentSetIndex = get(minBy(sets, 'set_index'), 'set_index', 0)
    currentSet = sets.find((set) => (set.set_prefix == currentSetPrefix && set.set_index == currentSetIndex))
  }

  // whenever the page or the currentSet changes
  useEffect(() => {
    // scroll to top
    window.scrollTo(0, 0)

    // focus the first text or textarea widget
    const firstWidget = document.querySelector('.interview-widget')
    if (firstWidget) {
      const focusInput = firstWidget.querySelector('.text-input input[type="text"], .textarea-input textarea')
      if (focusInput) {
        focusInput.focus()
      }
    }
  }, [page.id])

  return !isNil(page) && !isNil(sets) && !isNil(values) && (
    <div className="project-interview-page">
      <PageHelp />
      <PageManagement />
      <PageHead
        sets={sets.filter((set) => (set.set_prefix == currentSetPrefix) && (set.element == page))}
        values={isNil(page.attribute) ? [] : values.filter((value) => (value.attribute == page.attribute))}
        currentSet={currentSet}
      />
      <div className="project-interview-page-elements mt-2">
        <div className="card card-tile mb-4">
          <div className="card-body">
            <div className="d-flex flex-column justify-content-between gap-4">
              {
                currentSet && (
                  page.elements.map((element, elementIndex) => {
                    if (element.model == 'questions.questionset') {
                      return (
                        <QuestionSet
                          key={elementIndex}
                          questionset={element}
                          sets={sets}
                          values={values.filter((value) => element.attributes.includes(value.attribute))}
                          parentSet={currentSet}
                        />
                      )
                    } else {
                      return (
                        <Question
                          key={elementIndex}
                          question={element}
                          sets={
                            sets.filter((set) => (
                              set.set_prefix == currentSetPrefix
                            ))
                          }
                          values={
                            values.filter((value) => (
                              value.attribute == element.attribute &&
                              value.set_prefix == currentSetPrefix &&
                              value.set_index == currentSetIndex
                            ))
                          }
                          siblings={
                            values.filter((value) => (
                              value.attribute == element.attribute &&
                              value.set_prefix == currentSetPrefix &&
                              value.set_index != currentSetIndex
                            ))
                          }
                          currentSet={currentSet}
                        />
                      )
                    }
                  })
                )
              }
            </div>
          </div>
        </div>
        <PageButtons />
      </div>
    </div>
  )
}

export default Page
