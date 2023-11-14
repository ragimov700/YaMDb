from django_filters import FilterSet, CharFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    """Фильтр для произведений."""
    genre = CharFilter('genre__slug')
    category = CharFilter('category__slug')
    year = CharFilter('year')
    name = CharFilter('name')

    class Meta:
        class Meta:
            model = Title
            fields = '__all__'
