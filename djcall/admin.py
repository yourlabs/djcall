from django.contrib import admin

from .models import Caller, Call, Cron


class MetadataModelAdmin:
    list_display = [
        'status',
        'spooled',
        'started',
        'ended',
        'created',
    ]


@admin.register(Caller)
class CallerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'callback',
        'spooler',
    ] + MetadataModelAdmin.list_display

    search_fields = [
        'pk',
        'kwargs',
    ]

    list_filter = [
        'status',
        'spooler',
        'priority',
        'callback',
    ]


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'caller',
    ] + MetadataModelAdmin.list_display

    list_filter = [
        'status',
        'caller__callback',
    ]

    search_fields = [
        'caller__callback',
        'caller__kwargs',
        'caller__pk',
    ]


@admin.register(Cron)
class CronAdmin(admin.ModelAdmin):
    list_display = [
        'minute',
        'hour',
        'day',
        'month',
        'weekday',
        'caller',
    ]
    readonly_fields = [
        'caller',
        'minute',
        'hour',
        'day',
        'month',
        'weekday',
    ]
