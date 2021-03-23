from django import forms


class EmptyChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), empty_label=None, required=True, widget=None, label=None,
                 initial=None, help_text=None, *args, **kwargs):
        # prepend an empty label if it exists (and field is not required!)
        choices = tuple([(u'', empty_label)] + list(choices))

        super().__init__(choices=choices, required=required, widget=widget, label=label,
                         initial=initial, help_text=help_text, **kwargs)

        def valid_value(self, value):
            return True