const projectImportFixture = [
  {
    key: 'https://example.com/terms/project/data-description||0|0',
    model: 'projects.value',
    uri: 'https://example.com/terms/project/data-description',
    uri_prefix: 'https://example.com/terms',
    question_text: 'What kinds of data will be collected?',
    attribute_uri: 'https://example.com/terms/project/data-description',
    set_prefix: '',
    set_index: 0,
    set_collection: null,
    collection_index: 0,
    text: 'Interview transcripts and survey data',
    option_uri: null,
    file_name: null,
    value_type: 'text',
    unit: '',
    external_id: '',
    value_and_unit: 'Interview transcripts and survey data',
    created: false,
    updated: true,
    warnings: {},
    errors: [],
    updated_and_changed: {
      value_and_unit: {
        current_data: 'Interview transcripts',
        new_data: 'Interview transcripts and survey data'
      }
    }
  },
  {
    key: 'https://example.com/terms/project/storage-location||0|0',
    model: 'projects.value',
    uri: 'https://example.com/terms/project/storage-location',
    uri_prefix: 'https://example.com/terms',
    question_text: null,
    attribute_uri: 'https://example.com/terms/project/storage-location',
    set_prefix: '',
    set_index: 0,
    set_collection: null,
    collection_index: 0,
    text: 'Institutional repository',
    option_uri: null,
    file_name: null,
    value_type: 'text',
    unit: '',
    external_id: '',
    value_and_unit: 'Institutional repository',
    created: true,
    updated: false,
    warnings: {
      'https://example.com/terms/project/storage-location': [
        'Not available in this catalog.'
      ]
    },
    errors: [],
    updated_and_changed: {}
  },
  {
    key: 'https://example.com/terms/project/retention-period||0|0',
    model: 'projects.value',
    uri: 'https://example.com/terms/project/retention-period',
    uri_prefix: 'https://example.com/terms',
    question_text: 'How long will the data be retained?',
    attribute_uri: 'https://example.com/terms/project/retention-period',
    set_prefix: '',
    set_index: 0,
    set_collection: null,
    collection_index: 0,
    text: '10',
    option_uri: null,
    file_name: null,
    value_type: 'text',
    unit: 'years',
    external_id: '',
    value_and_unit: '10 years',
    created: false,
    updated: true,
    warnings: {},
    errors: [],
    updated_and_changed: {
      value_and_unit: {
        current_data: '10 years',
        new_data: '10 years'
      }
    }
  }
]

export default projectImportFixture
