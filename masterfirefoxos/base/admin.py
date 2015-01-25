from django.contrib import admin, messages

from feincms.module.page.models import Page
from feincms.module.page.admin import PageAdmin as PageAdminOld

from .models import QuizQuestion, QuizAnswer
from .utils import copy_tree


class PageAdmin(PageAdminOld):
    save_on_top = True
    actions = ['copy_tree_admin_action']

    def copy_tree_admin_action(self, request, queryset):
        if len(queryset) != 1:
            self.message_user(request, 'Select only one page to copy', level=messages.ERROR)
            return
        copy_tree(queryset[0])
    copy_tree_admin_action.short_description = 'Copy tree'


class QuizAnswerInline(admin.StackedInline):
    model = QuizAnswer
    extra = 0


class QuizQuestionAdmin(admin.ModelAdmin):
    search_fields = ['question']
    inlines = [QuizAnswerInline]


admin.site.unregister(Page)
admin.site.register(Page, PageAdmin)
admin.site.register(QuizQuestion, QuizQuestionAdmin)
