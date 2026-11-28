// combine the accepted file types of all upload plugins
export const combineUploadAccept = (uploadImports) => (
  uploadImports.reduce((accept, [, plugin]) => {
    Object.entries(plugin.accept).forEach(([mimeType, suffixes]) => {
      accept[mimeType] = [...new Set([...(accept[mimeType] ?? []), ...suffixes])]
    })
    return accept
  }, {})
)
