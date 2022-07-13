import pdb
import json

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.shortcuts import render
from django.template import loader

from rdmo.core.views import ModelPermissionMixin
from rdmo.core.constants import VALUE_TYPE_FILE
from rdmo.core.plugins import get_plugin
from rdmo.core.utils import markdown2html

from rdmo.questions.models import Catalog

from rdmo.catalogs_table.utils import get_language_field_name

class CatalogChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return mark_safe('<b>%s</b></br>%s' % (obj.title, markdown2html(obj.help)))


def htmx_httpresponse_headers(self, form, show_msg: str = None, redirect_url= None,**kwargs):

    print(f'HTMX httpresponse from: {self}')
    print('Msg: ', show_msg)
    
    response = HttpResponse(
                
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "catalogChanged": True,
                        "showMessage": show_msg
                    }),
                    
                })
    # pdb.set_trace()
    if redirect_url:
        response.headers['HX-Redirect'] = redirect_url

    print(response)
    print(response.headers)
    return response

class CatalogsModalUpdateView(ModelPermissionMixin, LoginRequiredMixin, UpdateView):
    ''' the form for the Modal inside catalogs_table '''
    permission_required = 'questions.view_catalog'
    model = Catalog
    fields = ('key', 'comment','locked','title_lang1', 'title_lang2', 'order', 'groups', 'sites')
    template_name = 'catalogs_table/partials/table_update_catalog_modal.html'
    success_url = reverse_lazy('catalogs_table')
    

    def form_valid(self, form):
        print(f'Form valid {self}')
        print(f'object', self.get_object().title)
        form.save()
        print(f'Form saved() {self}')
        field_title = get_language_field_name('title')
        form_update_msg = f"Catalog {form.cleaned_data.get(field_title)} was updated"
        # HX-Redirect= reverse("home:index")
        return htmx_httpresponse_headers(self, form, show_msg=form_update_msg)
        if 0:
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "catalogChanged": None,
                        "showMessage": f"CATALOGS added. {form.cleaned_data} "
                    }),
                    'HX-Redirect' : self.success_url
                })
            

class CatalogsLockedFormView(ModelPermissionMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    fields = ['locked']
    template_name = 'catalogs_table/columns/locked_form.html'
    success_url = reverse_lazy('table_list_locked')

    def form_valid(self, form):
        # print(f'Form valid {self}')
        # print(f'object', self.get_object())
        # pdb.set_trace()
        msg = f'{self.get_object().title} changed to {form.cleaned_data.get("locked")}'
        # print(form.cleaned_data)
        form.save()
        # print(f'Form saved() {self}')
        return htmx_httpresponse_headers(self, form, show_msg=msg)
       


class CatalogsSitesFormView(ModelPermissionMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'questions.view_catalog'
    model = Catalog
    fields = ['sites']
    template_name = 'catalogs_table/columns/sites_form.html'
    # success_url = reverse_lazy('table_list_sites', args=str(self.get_object().pk))

    def get_success_url(self) -> str:
        return reverse_lazy('table_list_sites', args=str(self.get_object().pk))
        # return super().get_success_url()

    def get_context_data(self, **kwargs):
        print('context: ', self)
        print('kwargs: ', kwargs)
        # "{% url 'table_list_sites' {{ pk }} %}" 
        redirect_url = self.get_success_url()
        # reverse_lazy('table_list_sites', args=str(self.get_object().pk))
        kwargs.update({'redirect_url' : redirect_url, 'pk' : str(self.get_object().pk)})
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # print(f'Form valid {self}')
        # print(f'object', self.get_object())
        form.save()
        # print(f'object', self.get_object().pk)
        # form.save()
        # print(f'Form saved() {self}')
        form_update_msg = f"Catalog {self.get_object().title} was updated with: {', '.join(map(str, form.cleaned_data.get('sites')))}"
        sites_form_url = reverse_lazy('table_update_sites', args=str(self.get_object().pk))
        # pdb.set_trace()
        rendered = render(self.request, 'catalogs_table/columns/sites.html', 
                                        {'sites': form.cleaned_data['sites'].values(),
                                         'sites_form_url' : sites_form_url,
                                         'pk' : str(self.get_object().pk)
                                        })
        return rendered
        # return htmx_httpresponse_headers(self, form, show_msg=form_update_msg)
        # print(f'Form saved() {self}')\
        if 0:
            content = loader.render_to_string(self.get_success_url())

            
            
            
            response = HttpResponse(
                    rendered,
                    content_type="text/html",
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                            "catalogChanged": True,
                            "showMessage": form_update_msg
                        }),
                        
                    })
            return response
            
        
        if 0:
            redirect_url=self.get_success_url()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "catalogChanged": None,
                        "showMessage": f"CATALOGS added. {form.cleaned_data} "
                    }),
                    'HX-Redirect' : self.success_url
                })



class CatalogTableForm(forms.ModelForm):

    use_required_attribute = False

    # def __init__(self, *args, **kwargs):
    #     catalogs = kwargs.pop('catalogs')
    #     super().__init__(*args, **kwargs)
    #     self.fields['title'].widget.attrs.update({
    #         'autofocus': True
    #     })
    #     self.fields['catalog'].queryset = catalogs
    #     self.fields['catalog'].empty_label = None
    #     self.fields['catalog'].initial = catalogs.first()
    class Meta:
        model = Catalog

        fields = ('title_lang1', 'uri', 'locked')
        labels = {
            'title_lang1' : 'Title'
        }

        # field_classes = {
        #     'catalog': CatalogChoiceField
        # }
        widgets = {
            'locked': forms.CheckboxInput()
                # attrs={'onclick':'this.form.submit();'}),required=False, label="Status")
        }
