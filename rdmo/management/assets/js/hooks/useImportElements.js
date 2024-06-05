import {useMemo} from 'react'
import isEmpty from 'lodash/isEmpty'

export const useImportElements = (elements) => {
  return useMemo(() => {
    // the elements are already processed by processElementDiffs in the importsReducer
    const createdElements = elements.filter(element => element.created)
    const updatedElements = elements.filter(element => element.updated)
    // changedElements collects elements with updated AND changed OR created
    const changedElements = elements.filter(element => ((element.updated && element.changed) || element.created))
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
