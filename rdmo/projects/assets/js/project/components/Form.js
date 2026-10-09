import React, { useState } from 'react'

import Input from 'rdmo/core/assets/js/components/Input'
import InputDebounced from 'rdmo/core/assets/js/components/InputDebounced'
import Textarea from 'rdmo/core/assets/js/components/Textarea'
import TextareaDebounced from 'rdmo/core/assets/js/components/TextareaDebounced'

const TestForm = ({  }) => {

  const [values, setValues] = useState({})
  const [errors, setErrors] = useState({})

  const handleSubmit = (event) => {
    event.preventDefault()
    console.log('submit!')
  }

  const fakeError = () => {
    setErrors({ text: ['There is something wrong here...']})
  }

  const reset = () => {
    setValues({})
    setErrors({})
  }

  console.log(values)

  return (
    <form className="mt-5 mb-5" onSubmit={handleSubmit}>
      <Input
        className="mb-4"
        label={gettext('Input')}
        help={gettext('Help, I need somebody, help!')}
        errors={errors.text}
        value={values.text || ''}
        onChange={(text) => setValues({ ...values, text })}
      />

      <InputDebounced
        className="mb-4"
        label={gettext('InputDebounced')}
        help={gettext('Help, I need somebody, help!')}
        errors={errors.textDebounced}
        value={values.textDebounced || ''}
        onChange={(textDebounced) => setValues({ ...values, textDebounced })}
      />

      <Textarea
        rows="4"
        className="mb-4"
        label={gettext('Textarea')}
        help={gettext('Help, I need somebody, help!')}
        errors={errors.textarea}
        value={values.textarea || ''}
        onChange={(textarea) => setValues({ ...values, textarea })}
      />

      <TextareaDebounced
        rows="4"
        className="mb-4"
        label={gettext('TextareaDebounced')}
        help={gettext('Help, I need somebody, help!')}
        errors={errors.textareaDebounced}
        value={values.textareaDebounced || ''}
        onChange={(textareaDebounced) => setValues({ ...values, textareaDebounced })}
      />

      <div className="d-flex gap-2">
        <button type="submit" className="btn btn-primary" onClick={handleSubmit}>{gettext('Submit')}</button>
        <button type="button" className="btn btn-danger" onClick={fakeError}>{gettext('Fake an error')}</button>
        <button type="button" className="btn btn-secondary" onClick={reset}>{gettext('Reset')}</button>
      </div>
    </form>
  )
}

export default TestForm
