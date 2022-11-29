import { fetchJson } from 'rdmo/core/assets/js/api/CoreApi'

class QuestionsApi {

  static fetchCatalogs(index=false) {
    let url = '/api/v1/questions/catalogs/'
    if (index) url += 'index/'
    return fetchJson(url)
  }

  static fetchCatalog(id, nested=false) {
    let url = `/api/v1/questions/catalogs/${id}/`
    if (nested) url += 'nested/'
    return fetchJson(url)
  }

  static fetchSections(index=false) {
    let url = `/api/v1/questions/sections/`
    if (index) url += 'index/'
    return fetchJson(url)
  }

  static fetchPages(index=false) {
    let url = `/api/v1/questions/pages/`
    if (index) url += 'index/'
    return fetchJson(url)
  }

  static fetchQuestionSets(index=false) {
    let url = `/api/v1/questions/questionsets/`
    if (index) url += 'index/'
    return fetchJson(url)
  }

  static fetchQuestions(index=false) {
    let url = `/api/v1/questions/questions/`
    if (index) url += 'index/'
    return fetchJson(url)
  }
}

export default QuestionsApi
