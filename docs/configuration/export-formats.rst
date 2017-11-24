Export formats
--------------

RDMO supports exports to certain formats using the excellent `pandoc <https://pandoc.org/>`_ converter. The list of formats to select can be customized by changing the ``EXPORT_FORMATS`` setting in your ``config/settings/local.py``.

.. code:: python

    EXPORT_FORMATS = (
        ('pdf', _('PDF')),
        ('rtf', _('Rich Text Format')),
        ('odt', _('Open Office')),
        ('docx', _('Microsoft Office')),
        ('html', _('HTML')),
        ('markdown', _('Markdown')),
        ('mediawiki', _('mediawiki')),
        ('tex', _('LaTeX'))
    )

The different formats supported by pandoc can be found `on the pandoc homepage <https://pandoc.org/>`_.
