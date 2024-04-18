from django import forms
from django.contrib import admin
from django.contrib.admin.templatetags.admin_list import _boolean_icon
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from mrsage.django.deployment_configuration import deployment_settings
from mrsage.django.deployment_configuration.core import (
    generate_type_string_from_type,
    hydrate_value,
)
from mrsage.django.deployment_configuration.django_settings_helpers import (
    get_library_setting,
)
from mrsage.django.deployment_configuration.models import Option, OptionType
from mrsage.django.deployment_configuration.store import change_value_for_option


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        exclude = []

    class Media:
        js = ["deployment_configuration/admin_live_update.js"]

    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(*args, instance=instance, **kwargs)

        if instance:
            self.fields['option_type'].queryset = OptionType.objects.filter(supportedoptions=instance)
            self.fields['raw_value'].required = False

    def clean(self):
        data = super().clean()
        if 'raw_value' not in data:
            data['raw_value'] = False

        raw_value = data['raw_value']
        option_type = data['option_type']

        try:
            hydrate_value(
                raw_value,
                option_type.python_callable,
            )
            change_value_for_option(
                self.instance,
                raw_value,
                option_type,
            )
        except Exception as e:
            raise ValidationError(str(e)) from e

        return data


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Basic Information",
            {
                "fields": ["name", "current_value", "current_cache_value", "matches_cache", ],
            },
        ),
        (
            "Make Changes",
            {
                "fields": ["raw_value", "option_type", ]
            }
        ),
        (
            "Defaults",
            {
                "classes": ["collapse"],
                "fields": ["default_type_with_label", "default_value", ],
            }
        ),
        (
            "Documentation",
            {
                "classes": ["collapse", "start-open", ],
                "fields": ["rendered_documentation", ],
            },
        ),
    ]
    if not get_library_setting('use_cache'):
        fieldsets[0][1]['fields'] = list(filter(lambda v: 'cache' not in v, fieldsets[0][1]['fields']))

    readonly_fields = [
        'name', 'current_value', 'current_cache_value',
        'default_type_with_label', 'default_value',
        'rendered_documentation', 'matches_cache'
    ]
    if not get_library_setting('use_cache'):
        readonly_fields = list(filter(lambda v: 'cache' not in v, readonly_fields))

    exclude = ['supported_types', 'documentation', 'default_type', 'allowed_types', ]
    list_display = [
        'updated',
        'current_value', 'current_cache_value', 'matches_cache',
        'default_value', 'default_type',
    ]
    if not get_library_setting('use_cache'):
        list_display = list(filter(lambda v: 'cache' not in v, list_display))

    actions = ["reset_to_default", "reset_cache_value", ]
    if not get_library_setting('use_cache'):
        actions = list(filter(lambda v: 'cache' not in v, actions))

    form = OptionForm

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).select_related('option_type', 'default_type')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)

        match db_field.name:
            case "option_type":
                formfield.empty_label = None
                formfield.widget.can_delete_related = False
                formfield.widget.can_change_related = False
                formfield.widget.can_add_related = False
                formfield.widget.can_view_related = False
                formfield.label_from_instance = lambda obj: obj.admin_label()

        return formfield

    @admin.display(description="Description")
    def rendered_documentation(self, instance):
        return mark_safe(instance.documentation)

    @admin.display(description="Default type")
    def default_type_with_label(self, instance):
        return instance.default_type.admin_label()

    @admin.display(description="Current value")
    def current_value(self, obj: Option):
        if obj.option_type.python_callable == 'builtins.bool':
            value = _boolean_icon(obj.value)
        else:
            value = obj.value

        return mark_safe(f"{obj.option_type.python_callable}: {value}")

    @admin.display(description="Current cached value")
    def current_cache_value(self, obj: Option):
        value = getattr(deployment_settings, obj.name)
        type_string = generate_type_string_from_type(type(value))

        return mark_safe(f"{type_string}: {value}")

    @admin.display(description="Cache matches")
    def matches_cache(self, obj: Option):
        return _boolean_icon(self.current_cache_value(obj) == self.current_value(obj))

    @admin.action(description="Reset to default")
    def reset_to_default(self, request, queryset):
        option: Option
        for option in queryset:
            option.reset_to_default()
            option.save()

    @admin.action(description="Reset cache to match current value")
    def reset_cache_value(self, request, queryset):
        option: Option
        for option in queryset:
            option.save()


@admin.register(OptionType)
class OptionTypeAdmin(admin.ModelAdmin):
    readonly_fields = ['python_callable', 'documentation']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
