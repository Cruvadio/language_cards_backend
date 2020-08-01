import datetime

from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Profile


class ProfileFilter(filters.FilterSet):
    username = filters.CharFilter(field_name="user", lookup_expr="username__icontains")
    min_age = filters.NumberFilter(method='filter_min_age')
    max_age = filters.NumberFilter(method='filter_max_age')
    friends = filters.BooleanFilter(method='filter_friends')

    class Meta:
        model = Profile
        fields = ["username", "min_age", "max_age"]

    def filter_min_age(self, queryset, name, value):
        today = datetime.date.today()
        date = datetime.date(today.year - value, today.month, today.day)
        return queryset.filter(birth_date__lte=date)

    def filter_max_age(self, queryset, name, value):
        today = datetime.date.today()
        date = datetime.date(today.year - value, today.month, today.day)
        return queryset.filter(Q(birth_date__year__gt=date.year) |
                               (Q(birth_date__year=date.year) & (Q(birth_date__month__lt=today.month) |
                                                                 (Q(birth_date__month=today.month) & Q(
                                                                     birth_date__day__lte=today.day)))))

    def filter_friends(self, queryset, name, value):
        user = self.request.user
        if type(value) is bool:
            profiles = user.profile.get_friends()
            if value:
                return queryset.filter(id__in=profiles)
            else:
                return queryset.exclude(id__in=profiles)
        return queryset.all()


