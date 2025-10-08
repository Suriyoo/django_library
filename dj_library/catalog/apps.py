from django.apps import AppConfig

#使用manage.py 创建的应用会将主键的类型设置为BigAutoField
class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
