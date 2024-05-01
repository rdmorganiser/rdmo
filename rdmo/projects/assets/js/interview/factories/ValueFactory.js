import { isNil, toNumber } from 'lodash'

import projectId from '../utils/projectId'

class ValueFactory {

  static create({ attribute, set_prefix, set_index, collection_index, set_collection,
                  text, option, file, external_id }) {
    return {
      project: projectId,
      attribute: attribute,
      set_prefix: isNil(set_prefix) ? '' : set_prefix,
      set_index: isNil(set_index) ? 0 : toNumber(set_index),
      collection_index: isNil(collection_index) ? 0 : toNumber(collection_index),
      set_collection: isNil(set_collection) ? false : set_collection,
      text: isNil(text) ? '' : text,
      option: isNil(option) ? null : option,
      file: isNil(file) ? null : file,
      external_id: isNil(external_id) ? '' : external_id
    }
  }

  static update(value, { text, option, file, external_id }) {
    value.text = isNil(text) ? '' : text
    value.option = isNil(option) ? null : option
    value.file = isNil(file) ? null : file
    value.external_id = isNil(external_id) ? '' : external_id
    return value
  }

}

export default ValueFactory
