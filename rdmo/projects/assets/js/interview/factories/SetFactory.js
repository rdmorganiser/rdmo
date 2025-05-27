import { isNil, toNumber } from 'lodash'

class SetFactory {

  static create({ set_prefix, set_index, questionset }) {
    return {
      set_prefix: isNil(set_prefix) ? '' : set_prefix,
      set_index: isNil(set_index) ? 0 : toNumber(set_index),
      questionset: isNil(questionset) ? null : questionset
    }
  }

}

export default SetFactory
