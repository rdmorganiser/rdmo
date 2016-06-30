from django.contrib import admin

from .models import *

admin.site.register(Catalog)
admin.site.register(Section)
admin.site.register(Subsection)
admin.site.register(QuestionEntity)
admin.site.register(Question)
