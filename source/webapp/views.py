from urllib.parse import urlencode

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import SimpleSearchForm, CreateForm, SimpleCreateForm
from webapp.models import File


class IndexView(ListView):
    model = File
    template_name = 'index.html'
    paginate_by = 10
    paginate_orphans = 1
    ordering = '-created_at'

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(
                Q(sign__icontains=self.search_value),
                access='general'
            )
        else:
            queryset = queryset.filter(access='general')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_search_form(self):
        return SimpleSearchForm(data=self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class FileView(DetailView):
    model = File
    template_name = 'file_detail.html'

    def get_object(self, queryset=None):
        file = File.objects.get(pk=self.kwargs.get('pk'))
        return file

    def dispatch(self, request, *args, **kwargs):
        file = self.get_object()
        if file.access == 'general' or file.access == 'hidden':
            return super().dispatch(request, *args, **kwargs)
        elif self.request.user == file.author or self.request.user in file.private.all():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class FileCreateView(CreateView):
    model = File
    template_name = 'file_create.html'

    def get_form_class(self):
        if self.request.user.username:
            return CreateForm
        else:
            return SimpleCreateForm

    def form_valid(self, form):
        if self.request.user.username:
            form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:file_detail', kwargs={'pk': self.object.pk})


class FileUpdateView(UpdateView):
    model = File
    template_name = 'file_update.html'
    context_object_name = 'file'

    def get_form_class(self):
        if self.request.user.username:
            return CreateForm
        else:
            return SimpleCreateForm

    def get_object(self, queryset=None):
        file = File.objects.get(pk=self.kwargs.get('pk'))
        return file

    def dispatch(self, request, *args, **kwargs):
        file = self.get_object()
        if self.request.user == file.author or self.request.user.has_perm('webapp.change_file'):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('accounts:login')

    def get_success_url(self):
        return reverse('webapp:file_detail', kwargs={'pk': self.object.pk})


class FileDeleteView(DeleteView):
    model = File
    template_name = 'file_delete.html'
    success_url = reverse_lazy('webapp:index')
    context_object_name = 'file'

    def get_object(self, queryset=None):
        file = File.objects.get(pk=self.kwargs.get('pk'))
        return file

    def dispatch(self, request, *args, **kwargs):
        file = self.get_object()
        if self.request.user == file.author or self.request.user.has_perm('webapp.change_file'):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('accounts:login')


class PrivateUserDelete(View):
    def post(self, request):
        file = File.objects.get(pk=int(request.POST['file_id']))
        user = User.objects.get(id=int(request.POST['user_id']))
        file.private.remove(user)
        return JsonResponse({'status':'200'})

