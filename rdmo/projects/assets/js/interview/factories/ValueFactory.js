import { isNil, toNumber } from 'lodash'

import projectId from '../utils/projectId'

class ValueFactory {

  static create({ attribute, set_prefix, set_index, collection_index, set_collection,
                  text, option, file, external_id, unit, value_type }) {
    const value = {
      project: projectId,
      attribute: attribute,
      set_prefix: isNil(set_prefix) ? '' : set_prefix,
      set_index: isNil(set_index) ? 0 : toNumber(set_index),
      collection_index: isNil(collection_index) ? 0 : toNumber(collection_index),
      set_collection: isNil(set_collection) ? false : set_collection
    }

    return this.update(value, { text, option, file, external_id, unit, value_type })
  }

  static update(value, { text, option, file, external_id, unit, value_type }) {
    value.text = isNil(text) ? '' : text
    value.option = isNil(option) ? null : option
    value.file = isNil(file) ? null : file
    value.external_id = isNil(external_id) ? '' : external_id
    value.unit = isNil(unit) ? '' : unit
    value.value_type = isNil(value_type) ? 'text' : value_type
    return value
  }

}

export default ValueFactory
