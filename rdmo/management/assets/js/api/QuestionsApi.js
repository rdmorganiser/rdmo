import isNil from 'lodash/isNil'

import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class QuestionsApi extends BaseApi {

  static fetchCatalogs(action) {
    let url = '/api/v1/questions/catalogs/'
    if (action == 'index') url += 'index/'
    if (action == 'nested') url += 'nested/'
    return this.get(url)
  }

  static fetchCatalog(id, action) {
    let url = `/api/v1/questions/catalogs/${id}/`
    if (action == 'nested') url += 'nested/'
    return this.get(url)
  }

  static storeCatalog(catalog, action) {
    if (isNil(catalog.id)) {
      return this.post('/api/v1/questions/catalogs/', catalog)
    } else {
      let url = `/api/v1/questions/catalogs/${catalog.id}/`
      if (['add-site', 'remove-site'].includes(action)) {
        url = `/api/v1/questions/catalog-toggle-site/${catalog.id}/${action}/`
      }
      return this.put(url, catalog)
    }
  }

  static deleteCatalog(catalog) {
    return this.delete(`/api/v1/questions/catalogs/${catalog.id}/`)
  }

  static fetchSections(action) {
    let url = '/api/v1/questions/sections/'
    if (action == 'index') url += 'index/'
    if (action == 'nested') url += 'nested/'
    return this.get(url)
  }

  static fetchSection(id, action) {
    let url = `/api/v1/questions/sections/${id}/`
    if (action == 'nested') url += 'nested/'
    return this.get(url)
  }

  static storeSection(section) {
    if (isNil(section.id)) {
      return this.post('/api/v1/questions/sections/', section)
    } else {
      return this.put(`/api/v1/questions/sections/${section.id}/`, section)
    }
  }

  static deleteSection(section) {
    return this.delete(`/api/v1/questions/sections/${section.id}/`)
  }

  static fetchPages(action) {
    let url = '/api/v1/questions/pages/'
    if (action == 'index') url += 'index/'
    if (action == 'nested') url += 'nested/'
    return this.get(url)
  }

  static fetchPage(id, action) {
    let url = `/api/v1/questions/pages/${id}/`
    if (action == 'nested') url += 'nested/'
    return this.get(url)
  }

  static storePage(page) {
    if (isNil(page.id)) {
      return this.post('/api/v1/questions/pages/', page)
    } else {
      return this.put(`/api/v1/questions/pages/${page.id}/`, page)
    }
  }

  static deletePage(page) {
    return this.delete(`/api/v1/questions/pages/${page.id}/`)
  }

  static fetchQuestionSets(action) {
    let url = '/api/v1/questions/questionsets/'
    if (action == 'index') url += 'index/'
    if (action == 'nested') url += 'nested/'
    return this.get(url)
  }

  static fetchQuestionSet(id, action) {
    let url = `/api/v1/questions/questionsets/${id}/`
    if (action == 'nested') url += 'nested/'
    return this.get(url)
  }

  static storeQuestionSet(questionset) {
    if (isNil(questionset.id)) {
      return this.post('/api/v1/questions/questionsets/', questionset)
    } else {
      return this.put(`/api/v1/questions/questionsets/${questionset.id}/`, questionset)
    }
  }

  static deleteQuestionSet(questionset) {
    return this.delete(`/api/v1/questions/questionsets/${questionset.id}/`)
  }

  static fetchQuestions(action) {
    let url = '/api/v1/questions/questions/'
    if (action == 'index') url += 'index/'
    return this.get(url)
  }

  static fetchQuestion(id) {
    return this.get(`/api/v1/questions/questions/${id}/`)
  }

  static storeQuestion(question) {
    if (isNil(question.id)) {
      return this.post('/api/v1/questions/questions/', question)
    } else {
      return this.put(`/api/v1/questions/questions/${question.id}/`, question)
    }
  }

  static deleteQuestion(question) {
    return this.delete(`/api/v1/questions/questions/${question.id}/`)
  }

  static fetchWidgetTypes() {
    return this.get('/api/v1/questions/widgettypes/')
  }

  static fetchValueTypes() {
    return this.get('/api/v1/questions/valuetypes/')
  }

}

export default QuestionsApi
