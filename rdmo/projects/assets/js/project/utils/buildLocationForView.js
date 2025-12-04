export const buildLocationForView = (viewId, snapshotId, { basePage = 'documents' } = {}) => {

  const hasView = viewId !== null && viewId !== undefined
  const hasSnapshot = snapshotId !== null && snapshotId !== undefined

  if (!hasView) {
    if (!hasSnapshot) {
      return {
        page: basePage,
        pageId: undefined,
        action: undefined,
        actionId: undefined,
      }
    }

    return {
      page: 'snapshots',
      pageId: String(snapshotId),
      action: undefined,
      actionId: undefined,
    }
  }

  const isAnswers = viewId === 'answers'

  if (!snapshotId) {
    return {
      page: 'documents',
      pageId: undefined,
      action: isAnswers ? 'answers' : 'views',
      actionId: isAnswers ? undefined : String(viewId),
    }
  }

  return {
    page: 'snapshots',
    pageId: String(snapshotId),
    action: isAnswers ? 'answers' : 'views',
    actionId: isAnswers ? undefined : String(viewId),
  }
}
