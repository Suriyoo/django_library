

#添加构建应用程序时的模式
from django.urls import path
from . import views

urlpatterns = [
     path('', views.index, name='index'), #如果检测到 URL 模式，则会调用一个视图函数
     path('books/', views.BookListView.as_view(), name='books'), #定义了一个用于匹配 URL 的模式 ( 'books/' )、一个在 URL 匹配时调用的视图函数 ( views.BookListView.as_view())，以及此特定映射的名称
     path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'), #'<int:pk>'获取书籍 ID，该 ID 必须是特殊格式的字符串，并将其作为主键传给视图
     path('author', views.AuthorListView.as_view(), name='authors'),
     path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]


urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'), 
]

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns +=[
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]
urlpatterns +=[
    path('genre/create/', views.GenreCreate.as_view(), name='genre-create'),
    
]
urlpatterns +=[
    path('language/create/', views.LanguageCreate.as_view(), name='language-create'),
    
]
urlpatterns +=[
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]

urlpatterns +=[
    path('bookinstances/create/', views.BookInstanceCreate.as_view(), name='bookinstance-create'),
]