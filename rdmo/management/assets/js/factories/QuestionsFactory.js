class QuestionsFactory {

  static createCatalog() {
    return {
      available: true
    }
  }

  static createSection() {
    return {}
  }

  static createPage() {
    return {}
  }

  static createQuestionSet() {
    return {}
  }

  static createQuestion() {
    return {
      widget_type: 'text',
      value_type: 'text'
    }
  }

}

export default QuestionsFactory
