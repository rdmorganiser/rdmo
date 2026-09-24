import { DiffMethod } from 'react-diff-viewer-continued'

function processElementDiffs(element) {
  let changedElement = false
  let changedFields = []

  const updatedAndChanged = element.updated_and_changed

  // Iterate over each field that might have changed
  const updatedWithDiffs = Object.entries(updatedAndChanged).reduce((acc, [key, { current_data, new_data }]) => {
    const elementFieldDiff = getDiff(current_data, new_data)

    // Determine if the field has changed
    if (elementFieldDiff.changed) {
      changedFields.push(key)
      changedElement = true
    }

    // Update the accumulator with new diff data
    acc[key] = elementFieldDiff
    return acc
  }, {})

  return {
    ...element,
    updated_and_changed: updatedWithDiffs,
    changedFields: changedFields,
    changed: changedElement
  }
}

function getDiff(currentData, updatedData) {
  let originalValueStr = currentData || ''
  let newValueStr = updatedData || ''
  let compareMethod = DiffMethod.CHARS

  if (Array.isArray(originalValueStr) && Array.isArray(newValueStr)) {
    // Cast array to string, joined by newline
    originalValueStr = originalValueStr.join('\n')
    newValueStr = newValueStr.join('\n')
    compareMethod = DiffMethod.LINES
  } else {
    // Cast to string
    originalValueStr = originalValueStr.toString()
    newValueStr = newValueStr.toString()
  }

  const changed = newValueStr !== originalValueStr

  // Return a structured object
  return {
    oldValue: originalValueStr,
    newValue: newValueStr,
    changed: changed,
    compareMethod: compareMethod
  }
}

export { processElementDiffs }
