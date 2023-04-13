from tours.models import Hotels


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cities = Hotels.objects.all()[:6]
        context['cities'] = cities

        return context