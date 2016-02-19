from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateView

from .views import *

urlpatterns = [
    url(_(r'^$'), questions, name='questions'),

    url(_(r'^sequence/$'), TemplateView.as_view(template_name='interviews/questions_sequence.html'), name='questions_sequence'),
    url(_(r'^sequence.gv/$'), questions_sequence_gv, name='questions_sequence_gv'),

    url(_(r'^catalogs/create$'), CatalogCreateView.as_view(), name='catalog_create'),
    url(_(r'^catalogs/(?P<pk>[0-9]+)/update$'), CatalogUpdateView.as_view(), name='catalog_update'),
    url(_(r'^catalogs/(?P<pk>[0-9]+)/delete$'), CatalogDeleteView.as_view(), name='catalog_delete'),

    url(_(r'^sections/create$'), SectionCreateView.as_view(), name='section_create'),
    url(_(r'^sections/(?P<pk>[0-9]+)/update$'), SectionUpdateView.as_view(), name='section_update'),
    url(_(r'^sections/(?P<pk>[0-9]+)/delete$'), SectionDeleteView.as_view(), name='section_delete'),
    url(_(r'^sections/(?P<pk>[0-9]+)/create-subsection/$'), SubsectionCreateSubsectionView.as_view(), name='section_create_subsection'),

    url(_(r'^subsections/create$'), SubsectionCreateView.as_view(), name='subsection_create'),
    url(_(r'^subsections/(?P<pk>[0-9]+)/update$'), SubsectionUpdateView.as_view(), name='subsection_update'),
    url(_(r'^subsections/(?P<pk>[0-9]+)/delete$'), SubsectionDeleteView.as_view(), name='subsection_delete'),
    url(_(r'^subsections/(?P<pk>[0-9]+)/create-question/$'), SubsectionCreateQuestionView.as_view(), name='subsection_create_question'),
    url(_(r'^subsections/(?P<pk>[0-9]+)/create-questionset/$'), SubsectionCreateQuestionSetView.as_view(), name='subsection_create_questionset'),

    url(_(r'^questions/create$'), QuestionCreateView.as_view(), name='question_create'),
    url(_(r'^questions/(?P<pk>[0-9]+)/update$'), QuestionUpdateView.as_view(), name='question_update'),
    url(_(r'^questions/(?P<pk>[0-9]+)/delete$'), QuestionDeleteView.as_view(), name='question_delete'),

    url(_(r'^questionsets/create$'), QuestionSetCreateView.as_view(), name='questionset_create'),
    url(_(r'^questionsets/(?P<pk>[0-9]+)/update$'), QuestionSetUpdateView.as_view(), name='questionset_update'),
    url(_(r'^questionsets/(?P<pk>[0-9]+)/delete$'), QuestionSetDeleteView.as_view(), name='questionset_delete'),
    url(_(r'^questionsets/(?P<pk>[0-9]+)/create-question/$'), QuestionSetCreateQuestionView.as_view(), name='questionset_create_question'),
]
