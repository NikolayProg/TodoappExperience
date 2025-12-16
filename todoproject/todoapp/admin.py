from django.contrib import admin
from .models import Category, Task

class CompleteFilter(admin.SimpleListFilter):
    title = 'Complete'
    parameter_name = 'complete'

    def lookups(self, request, model_admin):
        return [('complete', 'Complete'), ('uncomplete', 'Uncomplete')]

    def queryset(self, request, queryset):
        if self.value() == 'complete':
            return queryset.filter(completed=True)
        elif self.value() == 'uncomplete':
            return queryset.filter(completed=False)
        return queryset



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']
    search_fields = ['name']

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'complete', 'do_before', 'category']
    list_display = ['title', 'description', 'complete']
    search_fields = ['title', 'description', 'category']
    search_help_text = "Поиск по 'title', 'description', 'complete'"
    list_filter = ['complete', CompleteFilter]
    autocomplete_fields = ['category']
    list_editable = ['complete']

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

@admin.action(description="Пометить как завершенные")
def mark_complete(modeladmin, request, queryset):
    updated = queryset.update(complete=True)
    modeladmin.message_user(request, f'Завершено {updated} дел.')