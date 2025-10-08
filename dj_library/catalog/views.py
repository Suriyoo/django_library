from django.shortcuts import render

# Create your views here.

from .models import Book, Author, BookInstance, Genre, Language

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    #testing
    #精准匹配用exact，模糊用contains
    #title__exact='magic'或title='magic'  #大小写敏感
    #title__iexact='magic'  #大小写不敏感
    num_exact_word = Book.objects.filter(title__icontains='magic').count()
    num_exact_genre = Genre.objects.filter(name__icontains='fiction').count()

    num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_exact_word': num_exact_word,
        'num_exact_genre': num_exact_genre,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)



from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class BookListView(LoginRequiredMixin, generic.ListView): #在基于类的book实例视图中限制登录用户的访问权
    model = Book
    paginate_by = 2 #要访问第2页,用 URL /catalog/books/?page=2
    #context_object_name = 'book_list'   # your own name for the list as a template variable,默认也是 book_list，所以可以省略
    #queryset = Book.objects.filter(title__icontains='world')[:5] # Get 5 books containing the title 
    #template_name = 'book_list.html'  # Specify your own template name/location,默认是 book_list.html


class BookDetailView(generic.DetailView):
    model = Book
    

# def book_detail_view(request, primary_key):
#     try:
#         book = Book.objects.get(pk=primary_key)
#     except Book.DoesNotExist:
#         raise Http404('Book does not exist')

#     return render(request, 'catalog/book_detail.html', context={'book': book})

from django.shortcuts import get_object_or_404


def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 2


class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
    


from django.contrib.auth.mixins import PermissionRequiredMixin

class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
    



from django.views.generic.edit import CreateView, UpdateView, DeleteView #CreateView Django 内置的通用视图，用于处理模型实例的创建（渲染表单、验证数据、保存到数据库）
from django.urls import reverse_lazy
from .models import Author

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.add_book'
    def get_success_url(self):
        return reverse_lazy('book-detail',kwargs={'pk': self.object.pk})

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.change_book'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.delete_book'

    def form_valid(self,form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("book-delete", kwargs={"pk": self.object.pk})
            )


class GenreCreate(PermissionRequiredMixin, CreateView):
    model = Genre
    fields = ['name', ]
    permission_required = 'catalog.add_genre'

class LanguageCreate(PermissionRequiredMixin, CreateView):
    model = Language
    fields = ['name', ]
    permission_required = 'catalog.add_language'

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/11/2023'} #设置字段的初始值
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    permission_required = 'catalog.change_author'
    def get_success_url(self):
        return reverse_lazy('author-detail',kwargs={'pk': self.object.pk})


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )
        
class BookInstanceCreate(PermissionRequiredMixin, CreateView):
    model = BookInstance
    fields = ['name', ]
    permission_required = 'catalog.add_bookinstance'


import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404 #若数据库查询失败，返回404错误（替代直接调用 BookInstance.objects.get(pk=pk)）
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date'] #当验证通过后，Django 会将用户提交的数据进行类型转换和清理，结果存储在 form.cleaned_data 字典中
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)