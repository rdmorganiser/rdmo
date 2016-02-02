from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateView

from .views import *

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', interview, name='interview'),

    url(_(r'^(?P<interview_id>[0-9]+)/question/(?P<question_id>[0-9]+)$'), interview_question, name='interview_question'),

    url(_(r'^create$'), interview_create, name='interview_create'),
    url(_(r'^(?P<pk>[0-9]+)/update$'), interview_update, name='interview_update'),
    url(_(r'^(?P<pk>[0-9]+)/delete$'), interview_delete, name='interview_delete'),

    # /questions
    url(_(r'^questions/$'), questions, name='questions'),
    url(_(r'^questions/sequence/$'), TemplateView.as_view(template_name='interviews/questions_sequence.html'), name='questions_sequence'),
    url(_(r'^questions/sequence.dot/$'), questions_sequence_dot, name='questions_sequence_dot'),
    url(_(r'^questions/(?P<pk>[0-9]+)/$'), question, name='question'),
    url(_(r'^questions/create$'), QuestionCreateView.as_view(), name='question_create'),
    url(_(r'^questions/(?P<pk>[0-9]+)/update$'), QuestionUpdateView.as_view(), name='question_update'),
    url(_(r'^questions/(?P<pk>[0-9]+)/delete$'), QuestionDeleteView.as_view(), name='question_delete'),
]
