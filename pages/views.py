from django.views.generic import TemplateView, ListView

from books.models import Book


# Create your views here.
class HomePageView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'front_page.html'

    def three_latest(self):
        latest = self.model.objects.all()
        return latest[:3]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_books = self.three_latest()
        context.update({'three_latest': latest_books})
        return context


class AboutPageView(TemplateView):
    template_name = 'about.html'
