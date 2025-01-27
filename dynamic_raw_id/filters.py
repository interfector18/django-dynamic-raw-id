# coding: utf-8

"""dynamic_raw_id filters."""

from django import forms
from django.contrib import admin
from django.contrib.admin.options import TO_FIELD_VAR, IS_POPUP_VAR
from django.utils.http import urlencode

from dynamic_raw_id.widgets import DynamicRawIDWidget


class DynamicRawIDFilterForm(forms.Form):

    """Form for dynamic_raw_id filter."""

    def __init__(self, rel, admin_site, field_name, **kwargs):
        """Construct field for given field rel."""
        super(DynamicRawIDFilterForm, self).__init__(**kwargs)
        self.fields["%s__id" % field_name] = forms.CharField(
            label="",
            widget=DynamicRawIDWidget(rel=rel, admin_site=admin_site),
            required=False,
        )

    class Media:
        css = {
            "all": (
                "dynamic_raw_id/css/dynamic_raw_id_widget.css",
            )
        }
        js = (
            "dynamic_raw_id/js/filter.js",
        )


class DynamicRawIDFilter(admin.filters.FieldListFilter):

    """Filter list queryset by primary key of related object."""

    template = "dynamic_raw_id/admin/filters/dynamic_raw_id_filter.html"

    def __init__(self, field, request, params, model, model_admin, field_path):
        """Use GET param for lookup and form initialization."""
        self.lookup_kwarg = "%s__id" % field_path
        super(DynamicRawIDFilter, self).__init__(
            field, request, params, model, model_admin, field_path
        )
        rel = field.remote_field
        self.form = self.get_form(request, rel, model_admin.admin_site)
        self.request = request

    def choices(self, changelist):
        """
        Using this to catch all other applied filters
        """
        other_choices = {
            'query_pairs': [
                (k, v)
                for k, v in changelist.get_filters_params().items()
                if k != self.lookup_kwarg
            ],
        }
        for var in (TO_FIELD_VAR, IS_POPUP_VAR):
            if var in self.request.GET:
                other_choices["query_pairs"].append(
                    (var, self.request.GET[var]))
        yield other_choices

    def expected_parameters(self):
        """Return GET params for this filter."""
        return [self.lookup_kwarg]

    def get_form(self, request, rel, admin_site):
        """Return filter form."""
        return DynamicRawIDFilterForm(
            admin_site=admin_site,
            rel=rel,
            field_name=self.field_path,
            data=self.used_parameters,
        )

    def queryset(self, request, queryset):
        """Filter queryset using params from the form."""
        if self.form.is_valid():
            # get no null params
            filter_params = dict(
                filter(lambda x: bool(x[1]), self.form.cleaned_data.items())
            )
            return queryset.filter(**filter_params)
        return queryset

    def reset_query(self):
        param = self.lookup_kwarg
        query = {
            key: val
            for key, val in self.request.GET.items()
            if key != param
        }
        return urlencode(query)
