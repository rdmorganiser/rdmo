import { DiffMethod } from 'react-diff-viewer-continued'

function getDiff(currentData, updatedData) {
  let originalValueStr = currentData || ''
  let newValueStr = updatedData || ''
  let hideLineNumbers = true
  let splitView = false
  let compareMethod = DiffMethod.CHARS

  if (Array.isArray(originalValueStr) && Array.isArray(newValueStr)) {
    // Cast array to string, joined by newline
    originalValueStr = originalValueStr.join('\n')
    newValueStr = newValueStr.join('\n')
    hideLineNumbers = false
    splitView = false
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
    hideLineNumbers: hideLineNumbers,
    splitView: splitView,
    compareMethod: compareMethod
  }
}

export default getDiff
