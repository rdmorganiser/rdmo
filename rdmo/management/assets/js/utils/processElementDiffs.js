// utils/processElementDiffs.js
import getDiff from './getDiff' // Make sure the path is correct

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

export default processElementDiffs
