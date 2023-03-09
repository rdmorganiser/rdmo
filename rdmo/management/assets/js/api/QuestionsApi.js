import isNil from 'lodash/isNil'

import { getData, postData, putData } from 'rdmo/core/assets/js/utils/api'

class QuestionsApi {

  static fetchCatalogs(action) {
    let url = '/api/v1/questions/catalogs/'
    if (action == 'index') url += 'index/'
    if (action == 'nested') url += 'nested/'
    return getData(url)
  }

  static fetchCatalog(id, action) {
    let url = `/api/v1/questions/catalogs/${id}/`
    if (action == 'nested') url += 'nested/'
    return getData(url)
  }

  static storeCatalog(catalog) {
    if (isNil(catalog.id)) {
      return postData(`/api/v1/questions/catalogs/`, catalog)
    } else {
      return putData(`/api/v1/questions/catalogs/${catalog.id}/`, catalog)
    }
  }

  static fetchSections(action) {
    let url = `/api/v1/questions/sections/`
    if (action == 'index') url += 'index/'
    if (action == 'nested') url += 'nested/'
    return getData(url)
  }

  static fetchSection(id, action) {
    let url = `/api/v1/questions/sections/${id}/`
    if (action == 'nested') url += 'nested/'
    return getData(url)
  }

  static storeSection(section) {
    if (isNil(section.id)) {
      return postData(`/api/v1/questions/sections/`, section)
    } else {
      return putData(`/api/v1/questions/sections/${section.id}/`, section)
    }
  }

  static fetchPages(action) {
    let url = `/api/v1/questions/pages/`
    if (action == 'index') url += 'index/'
    if (action == 'nested') url += 'nested/'
    return getData(url)
  }

  static fetchPage(id, action) {
    let url = `/api/v1/questions/pages/${id}/`
    if (action == 'nested') url += 'nested/'
    return getData(url)
  }

  static storePage(page) {
    if (isNil(page.id)) {
      return postData(`/api/v1/questions/pages/`, page)
    } else {
      return putData(`/api/v1/questions/pages/${page.id}/`, page)
    }
  }

  static fetchQuestionSets(action) {
    let url = `/api/v1/questions/questionsets/`
    if (action == 'index') url += 'index/'
    if (action == 'nested') url += 'nested/'
    return getData(url)
  }

  static fetchQuestionSet(id, action) {
    let url = `/api/v1/questions/questionsets/${id}/`
    if (action == 'nested') url += 'nested/'
    return getData(url)
  }

  static storeQuestionSet(questionset) {
    if (isNil(questionset.id)) {
      return postData(`/api/v1/questions/questionsets/`, questionset)
    } else {
      return putData(`/api/v1/questions/questionsets/${questionset.id}/`, questionset)
    }
  }

  static fetchQuestions(action) {
    let url = `/api/v1/questions/questions/`
    if (action == 'index') url += 'index/'
    return getData(url)
  }

  static fetchQuestion(id) {
    return getData(`/api/v1/questions/questions/${id}/`)
  }

  static storeQuestion(question) {
    if (isNil(question.id)) {
      return postData(`/api/v1/questions/questions/`, question)
    } else {
      return putData(`/api/v1/questions/questions/${question.id}/`, question)
    }
  }

  static fetchWidgetTypes(id) {
    return getData(`/api/v1/questions/widgettypes/`)
  }

  static fetchValueTypes(id) {
    return getData(`/api/v1/questions/valuetypes/`)
  }

}

export default QuestionsApi
