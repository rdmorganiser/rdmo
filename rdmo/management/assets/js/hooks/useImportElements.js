import {useMemo} from 'react'
import isEmpty from 'lodash/isEmpty'
import processElementDiffs from '../utils/processElementDiffs'


export const useImportElements = (elements) => {
  return useMemo(() => {
    const elementsImported = elements.map(element => processElementDiffs(element))

    const createdElements = elementsImported.filter(element => element.created)
    const updatedElements = elementsImported.filter(element => element.updated)
    const changedElements = updatedElements.filter(element => element.changed)
    const importWarnings = elementsImported.filter(element => !isEmpty(element.warnings))
    const importErrors = elementsImported.filter(element => !isEmpty(element.errors))

    return {
      elementsImported,
      createdElements,
      updatedElements,
      changedElements,
      importWarnings,
      importErrors
    }
  }, [elements])
}
