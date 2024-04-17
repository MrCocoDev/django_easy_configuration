from django import forms
from django.contrib import admin
from django.contrib.admin.templatetags.admin_list import _boolean_icon
from django.utils.safestring import mark_safe

from mrsage.django.deployment_configuration.models import Option, OptionType

# TODO add reset to default action


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

    def clean(self):
        super().clean()
        try:
            ...
        except Exception:
            ...

        return True

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Basic Information",
            {
                "fields": ["name", "current_value", ],
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
                "fields": ["rendered_documentation", ],
            },
        ),
    ]
    readonly_fields = ['name', 'current_value', 'default_type_with_label', 'default_value', 'rendered_documentation', ]
    exclude = ['supported_types', 'documentation', 'default_type', 'allowed_types', ]
    list_display = ('current_value', 'option_type', 'default_value', 'default_type',)

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
