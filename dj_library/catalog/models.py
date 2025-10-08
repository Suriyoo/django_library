# 一个模型可以包含任意数量、任意类型的字段——每个字段代表想要存储在数据库表中的一列数据。每条数据库记录行都由每个字段值组成

from django.db import models
from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field
from django.conf import settings # Required to assign User as a borrower

# class MyModelName(models.Model):
#     """A typical class defining a model, derived from the Model class."""

#     # Fields 

#     # 一个字段my_field_name，其类型为models.CharField,包含字母数字字符串
#     #字段名称用于在查询和模板中引用它。字段也有一个标签，使用verbose_name参数指定（默认值为None）。
#     #如果verbose_name未设置 则标签将根据字段名称创建--将下划线替换为空格并首字母大写（如在表单中使用时，该字段的my_field_name默认标签为“my_field_name”）
#     my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')
#     # …

#     # Metadata 

#     #可以通过声明来为模型声明模型级元数据class Meta,此元数据最有用的功能之一是控制查询模型类型时返回记录的默认顺序ordering
#     class Meta:
#         ordering = ['-my_field_name'] #顺序取决于字段的类型（字符字段按字母顺序排序，而日期字段按时间顺序排序）。 (-) 为反转排序顺序

#     # Methods 

#     # 此字符串用于表示管理站点中的单个记录（以及任何需要引用模型实例的地方）。通常它会返回模型中的title或name字段
#     def get_absolute_url(self):
#         """Returns the URL to access a particular instance of MyModelName."""
#         return reverse('model-detail-view', args=[str(self.id)])

#     #用于在网站上显示单个模型记录（会自动在管理站点中模型的记录编辑界面添加一个“在站点上查看”按钮）
#     def __str__(self):
#         """String for representing the MyModelName object (in Admin site etc.)."""
#         return self.my_field_name

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=200,
        unique=True,#可以防止创建名称完全相同的类型，但大小写敏感
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """该方法返回一个URL用于访问此模型的详细记录。须定义一个包含名称的URL映射genre-detail并定义关联的视图和模板"""
        return reverse('genre-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),#指定字段值的小写形式name在数据库中必须唯一
                name='genre_name_case_insensitive_unique',
                violation_error_message = "Genre already exists (case insensitive match)"
            ),
        ]
class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            unique=True,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def get_absolute_url(self):
        """Returns the url to access a particular language instance."""
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message = "Language already exists (case insensitive match)"
            ),
        ]

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)#允许存空值，有引用则不能删除
    # Foreign Key used because book can only have one author, but authors can have multiple books.
    # Author as a string rather than object because it hasn't been declared yet in file.

    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(
        Genre, help_text="Select a genre for this book")

    language = models.ForeignKey(
        'Language', on_delete=models.SET_NULL, null=True)
    
    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

import uuid # Required for unique book instances
from django.contrib.auth.models import User
from datetime import date
class BookInstance(models.Model):

    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    #关联到 Book 模型
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True) # 如果书籍被借出（存在关联记录），禁止删除 Book 实例（保护数据完整性）
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    #关联到 Django 的 用户模型（推荐使用 settings.AUTH_USER_MODEL 而不是直接写 User，以支持自定义用户模型）
    #borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True) #当关联的用户被删除时，此字段设为 NULL（需配合 null=True）

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    @property
    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'
    
class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'