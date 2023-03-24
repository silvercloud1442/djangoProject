

class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        context['section_type'] = ''

        return context