from urllib.parse import urlencode

from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import SimpleSearchForm
from webapp.models import File


class IndexView(ListView):
    model = File
    template_name = 'index.html'
    paginate_by = 2
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
                Q(sign__icontains=self.search_value)
            )
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


class FileCreateView(CreateView):
    model = File
    template_name = 'file_create.html'
    fields = ('sign', 'file')
    # permission_required = 'webapp.add_product', 'webapp.can_have_piece_of_pizza'
    # permission_denied_message = '403 Доступ запрещён!'

    def form_valid(self, form):
        if self.request.user.username:
            form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:file_detail', kwargs={'pk': self.object.pk})


class FileUpdateView(UpdateView):
    model = File
    template_name = 'file_update.html'
    fields = ('sign', 'file')
    context_object_name = 'file'

    # def test_func(self):
    #     if self.request.user.has_perm('webapp.change_file'):
    #         return self.request.author.pk == self.request.user.pk

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

