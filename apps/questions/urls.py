from django.conf.urls import url, include
from django.utils.translation import ugettext_lazy as _

from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'catalogs', CatalogViewSet, base_name='catalog')
router.register(r'sections', SectionViewSet, base_name='section')
router.register(r'subsections', SubsectionViewSet, base_name='subsection')
router.register(r'questions', QuestionViewSet, base_name='question')
router.register(r'questionsets', QuestionSetViewSet, base_name='questionset')
router.register(r'widgettypes', WidgetTypeViewSet, base_name='widgettype')

urlpatterns = [

    url(_(r'^catalogs/$'), catalogs, name='catalogs'),
    url(_(r'^catalogs/(?P<pk>[0-9]+)/$'), catalog, name='catalog'),

    url(_(r'^catalogs/create$'), CatalogCreateView.as_view(), name='catalog_create'),
    url(_(r'^catalogs/(?P<pk>[0-9]+)/update$'), CatalogUpdateView.as_view(), name='catalog_update'),
    url(_(r'^catalogs/(?P<pk>[0-9]+)/delete$'), CatalogDeleteView.as_view(), name='catalog_delete'),
    url(_(r'^catalogs/(?P<pk>[0-9]+)/create-section/$'), CatalogCreateSectionView.as_view(), name='catalog_create_section'),

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

    url(r'^$', questions, name='questions'),
    url(r'^api/', include(router.urls)),
]
