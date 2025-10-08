from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language

#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)
admin.site.register(Language)

# Define the admin class
# class AuthorAdmin(admin.ModelAdmin):
#     pass


# Register the Admin classes for Book using the decorator

# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     pass


# Register the Admin classes for BookInstance using the decorator
# @admin.register(BookInstance)
# class BookInstanceAdmin(admin.ModelAdmin):
#     pass

class BooksInline(admin.TabularInline):
     model = Book
     extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')] #()用于横排选项
    inlines = [BooksInline]


class BooksInstanceInline(admin.TabularInline):
        model = BookInstance
        extra = 0
        show_change_link = True  # 允许点击进入独立编辑页
        fields = ['id', 'status', 'due_back']  # 只显示关键字段
        # readonly_fields = ['id']  # ID作为可点击链接 不好使不会显示

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

admin.site.register(Book, BookAdmin)

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','book','status', 'borrower','due_back')
    list_filter = ('status','due_back')
    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
admin.site.register(BookInstance,BookInstanceAdmin)
