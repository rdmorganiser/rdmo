import {useMemo} from 'react'
import isEmpty from 'lodash/isEmpty'

export const useImportElements = (elements) => {
  return useMemo(() => {
    // the elements are already processed by processElementDiffs in the importsReducer
    const createdElements = elements.filter(element => element.created)
    const updatedElements = elements.filter(element => element.updated)
    // collects elements with updated AND changed
    const changedElements = updatedElements.filter(element => element.changed)
    const importWarnings = elements.filter(element => !isEmpty(element.warnings))
    const importErrors = elements.filter(element => !isEmpty(element.errors))

    return {
      createdElements,
      updatedElements,
      changedElements,
      importWarnings,
      importErrors
    }
  }, [elements])
}
