import React, { useState } from 'react'

import Input from 'rdmo/core/assets/js/components/forms/Input'
import Select from 'rdmo/core/assets/js/components/forms/Select'
import Textarea from 'rdmo/core/assets/js/components/forms/Textarea'

const TestForm = ({  }) => {

  const [values, setValues] = useState({text: '1', textDebounced: '2'})
  const [errors, setErrors] = useState({})

  const handleSubmit = (event) => {
    event.preventDefault()
    console.log('submit!')
  }

  const fakeErrors = () => {
    setErrors({
      text: ['There is something wrong here...'],
      textDebounced: ['There is something wrong here...'],
      textarea: ['There is something wrong here...'],
      textareaDebounced: ['There is something wrong here...'],
      select: ['There is something wrong here...'],
      selectClearable: ['There is something wrong here...'],
      selectMulti: ['There is something wrong here...']
    })
  }

  const reset = () => {
    setValues({})
    setErrors({})
  }

  const options = [
    {value: 'a', label: 'a'},
    {value: 'b', label: 'b'},
    {value: 'c', label: 'c'}
  ]

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

      <Input
        className="mb-4"
        debounce={500}
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

      <Textarea
        rows="4"
        className="mb-4"
        debounce={500}
        label={gettext('TextareaDebounced')}
        help={gettext('Help, I need somebody, help!')}
        errors={errors.textareaDebounced}
        value={values.textareaDebounced || ''}
        onChange={(textareaDebounced) => setValues({ ...values, textareaDebounced })}
      />

      <Select
        className="mb-4"
        label={gettext('Select')}
        help={gettext('Help, I need somebody, help!')}
        options={options}
        errors={errors.select}
        value={values.select || ''}
        onChange={(select) => setValues({ ...values, select })}
      />

      <Select
        className="mb-4"
        label={gettext('SelectClearable')}
        help={gettext('Help, I need somebody, help!')}
        placeholder={gettext('SelectClearable...')}
        isClearable={true}
        options={options}
        errors={errors.selectClearable}
        value={values.selectClearable || ''}
        onChange={(selectClearable) => setValues({ ...values, selectClearable })}
      />

      <Select
        className="mb-4"
        label={gettext('SelectMulti')}
        help={gettext('Help, I need somebody, help!')}
        placeholder={gettext('SelectMulti...')}
        isClearable={true}
        isMulti={true}
        options={options}
        errors={errors.selectMulti}
        value={values.selectMulti || ''}
        onChange={(selectMulti) => setValues({ ...values, selectMulti })}
      />

      <div className="d-flex gap-2 mb-4">
        <button type="submit" className="btn btn-primary" onClick={handleSubmit}>{gettext('Submit')}</button>
        <button type="button" className="btn btn-danger" onClick={fakeErrors}>{gettext('Fake errors')}</button>
        <button type="button" className="btn btn-secondary" onClick={reset}>{gettext('Reset')}</button>
      </div>

      <pre>
        <code>
          {JSON.stringify(values)}
        </code>
      </pre>
    </form>
  )
}

export default TestForm
