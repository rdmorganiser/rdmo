import isNil from 'lodash/isNil'

import { getData, postData, putData } from 'rdmo/core/assets/js/utils/api'

class QuestionsApi {

  static fetchCatalogs(index=false, nested=false) {
    let url = '/api/v1/questions/catalogs/'
    if (index) url += 'index/'
    if (nested) url += 'nested/'
    return getData(url)
  }

  static fetchCatalog(id, nested=false) {
    let url = `/api/v1/questions/catalogs/${id}/`
    if (nested) url += 'nested/'
    return getData(url)
  }

  static storeCatalog(catalog) {
    if (isNil(catalog.id)) {
      return postData(`/api/v1/questions/catalogs/`, catalog)
    } else {
      return putData(`/api/v1/questions/catalogs/${catalog.id}/`, catalog)
    }
  }

  static fetchSections(index=false, nested=false) {
    let url = `/api/v1/questions/sections/`
    if (index) url += 'index/'
    if (nested) url += 'nested/'
    return getData(url)
  }

  static fetchSection(id, nested=false) {
    let url = `/api/v1/questions/sections/${id}/`
    if (nested) url += 'nested/'
    return getData(url)
  }

  static storeSection(section) {
    if (isNil(section.id)) {
      return postData(`/api/v1/questions/sections/`, section)
    } else {
      return putData(`/api/v1/questions/sections/${section.id}/`, section)
    }
  }

  static fetchPages(index=false, nested=false) {
    let url = `/api/v1/questions/pages/`
    if (index) url += 'index/'
    if (nested) url += 'nested/'
    return getData(url)
  }

  static fetchPage(id, nested=false) {
    let url = `/api/v1/questions/pages/${id}/`
    if (nested) url += 'nested/'
    return getData(url)
  }

  static storePages(page) {
    if (isNil(page.id)) {
      return postData(`/api/v1/questions/pages/`, page)
    } else {
      return putData(`/api/v1/questions/pages/${page.id}/`, page)
    }
  }

  static fetchQuestionSets(index=false, nested=false) {
    let url = `/api/v1/questions/questionsets/`
    if (index) url += 'index/'
    if (nested) url += 'nested/'
    return getData(url)
  }

  static fetchQuestionSet(id, nested=false) {
    let url = `/api/v1/questions/questionsets/${id}/`
    if (nested) url += 'nested/'
    return getData(url)
  }

  static storeQuestionSet(questionset) {
    if (isNil(questionset.id)) {
      return postData(`/api/v1/questions/questionsets/`, questionset)
    } else {
      return putData(`/api/v1/questions/questionsets/${questionset.id}/`, questionset)
    }
  }

  static fetchQuestions(index=false) {
    let url = `/api/v1/questions/questions/`
    if (index) url += 'index/'
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
