from django.contrib import admin
from django.utils.html import format_html

from .models import Priority, Category, Task, Note, SubTask


admin.site.site_header = "Hangarin Admin"
admin.site.site_title = "Hangarin Admin Portal"
admin.site.index_title = "Welcome to Hangarin Task Manager"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status_badge",
        "deadline",
        "priority_badge",
        "category",
        "created_at",
    )
    list_filter = ("status", "priority", "category", "deadline")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    list_per_page = 10
    date_hierarchy = "deadline"

    fieldsets = (
        ("Task Information", {
            "fields": ("title", "description")
        }),
        ("Task Details", {
            "fields": ("status", "deadline", "priority", "category")
        }),
    )

    def status_badge(self, obj):
        colors = {
            "Pending": ("#92400e", "#fef3c7"),
            "In Progress": ("#1d4ed8", "#dbeafe"),
            "Completed": ("#047857", "#d1fae5"),
        }

        text_color, bg_color = colors.get(obj.status, ("#374151", "#e5e7eb"))

        return format_html(
            '<span style="color: {}; background: {}; padding: 6px 10px; '
            'border-radius: 999px; font-weight: 700; font-size: 12px;">{}</span>',
            text_color,
            bg_color,
            obj.status
        )

    status_badge.short_description = "Status"

    def priority_badge(self, obj):
        colors = {
            "Critical": ("#991b1b", "#fee2e2"),
            "High": ("#9a3412", "#ffedd5"),
            "Medium": ("#854d0e", "#fef9c3"),
            "Low": ("#166534", "#dcfce7"),
            "Optional": ("#374151", "#e5e7eb"),
        }

        text_color, bg_color = colors.get(obj.priority.name, ("#374151", "#e5e7eb"))

        return format_html(
            '<span style="color: {}; background: {}; padding: 6px 10px; '
            'border-radius: 999px; font-weight: 700; font-size: 12px;">{}</span>',
            text_color,
            bg_color,
            obj.priority.name
        )

    priority_badge.short_description = "Priority"


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status_badge", "parent_task_name", "created_at")
    list_filter = ("status",)
    search_fields = ("title",)
    ordering = ("-created_at",)
    list_per_page = 10

    def parent_task_name(self, obj):
        return obj.parent_task.title

    parent_task_name.short_description = "Parent Task"

    def status_badge(self, obj):
        colors = {
            "Pending": ("#92400e", "#fef3c7"),
            "In Progress": ("#1d4ed8", "#dbeafe"),
            "Completed": ("#047857", "#d1fae5"),
        }

        text_color, bg_color = colors.get(obj.status, ("#374151", "#e5e7eb"))

        return format_html(
            '<span style="color: {}; background: {}; padding: 6px 10px; '
            'border-radius: 999px; font-weight: 700; font-size: 12px;">{}</span>',
            text_color,
            bg_color,
            obj.status
        )

    status_badge.short_description = "Status"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 10


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 10


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("task", "short_content", "created_at")
    list_filter = ("created_at",)
    search_fields = ("content",)
    ordering = ("-created_at",)
    list_per_page = 10

    def short_content(self, obj):
        if len(obj.content) > 60:
            return obj.content[:60] + "..."
        return obj.content

    short_content.short_description = "Content"