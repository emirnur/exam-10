from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.models import File


class IndexView(ListView):
    model = File
    template_name = 'index.html'
    paginate_by = 10

    def get_queryset(self):
        return File.objects.all().order_by('-created_at')


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
        if self.request.user is not None:
            form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:file_detail', kwargs={'pk': self.object.pk})


class FileUpdateView(UpdateView):
    model = File
    template_name = 'file_update.html'
    fields = ('sign', 'file')
    context_object_name = 'file'

    def get_success_url(self):
        return reverse('webapp:file_detail', kwargs={'pk': self.object.pk})


class FileDeleteView(DeleteView):
    model = File
    template_name = 'file_delete.html'
    success_url = reverse_lazy('webapp:index')
    context_object_name = 'file'

