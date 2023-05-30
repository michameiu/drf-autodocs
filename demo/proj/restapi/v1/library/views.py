from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from drf_autodocs.decorators import format_docstring
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
import django_filters
from mylib.my_common import MyDjangoFilterBackend

from .serializers import BookUpdateSerializer, LibrarySerializer, BookSerializer
from .request_response_examples import request_example, response_example
from library.models import Book, Library


# works for badly-designed views too
class BooksHandler(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


@format_docstring(request_example, response_example=response_example)
class BookReadUpdateHandler(RetrieveUpdateAPIView):
    """
    Wow, this magic decorator allows us to:
        1) Keep clean & short docstring
        2) Insert additional data in it, like request/response examples

    Request: {}
    Response: {response_example}
    """

    serializer_class = BookUpdateSerializer
    response_serializer_class = LibrarySerializer
    queryset = Book.objects.all()


class AttendanceFilter(FilterSet):
    GENDERS = (
        ("M", "Male"),
        ("F", "Female"),
    )
    base_class = django_filters.CharFilter(field_name="stream__base_class", label="Class")
    date = django_filters.DateFilter(field_name="date__date", label="date")
    start_date = django_filters.DateFilter(field_name="date", lookup_expr="gte", label="Start Date")
    end_date = django_filters.DateFilter(field_name="date", lookup_expr=("lte"), label="End Date")
    school = django_filters.NumberFilter(field_name="stream__school", label="School")
    school_emis_code = django_filters.NumberFilter(field_name="stream__school__emis_code", label="School Emis Code", lookup_expr="icontains")
    school_sub_county = django_filters.NumberFilter(field_name="stream__school__sub_county_id", label="School Sub County Id")
    school_county = django_filters.NumberFilter(field_name="stream__school__sub_county__county_id", label="School County Id")

    year = django_filters.NumberFilter(field_name="date__year", label="Year")
    month = django_filters.NumberFilter(field_name="date__month", label="Month")
    in_training_school = django_filters.BooleanFilter(field_name="stream__school__is_training_school")

    # partner=django_filters.NumberFilter(name="partner",method="filter_partner")
    # partner_admin=django_filters.NumberFilter(name="partner",method="filter_partner_admin",label="Partner Admin Id")
    # county_name=django_filters.CharFilter(name="stream__school__zone__subcounty__county__county_name",lookup_expr="icontains")
    # county = django_filters.NumberFilter(name="stream__school__zone__subcounty__county_id", label="County Id")

    # date_range = django_filters.DateRangeFilter(name='date')
    class Meta:
        model = Book
        fields = "__all__"

    def filter_partner(self, queryset, name, value):
        return queryset.filter(stream__school__partners__id=value)

    def filter_is_oosc(self, queryset, name, value):
        return queryset.filter(student__is_oosc=str2bool(value))

    def filter_partner_admin(self, queryset, name, value):
        return queryset.filter(stream__school__partners__partner_admins__id=value)


class LibrariesHandler(ListCreateAPIView):
    """
    Shiny and nice docstring, which:
        1) allows formatting
        2) `allows markdown`
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissions)
    filter_backends = [MyDjangoFilterBackend]
    # filter_backends = (OrderingFilter, SearchFilter, MyDjangoFilterBackend)
    filter_mixin = AttendanceFilter
    queryset = Library.objects.all()

    serializer_class = LibrarySerializer

    extra_url_params = (("show_all", "Bool", "if True returns all instances and only 5 otherwise"), ("some_extra_param", "Integer", "Something more to be included there"))

    def get_queryset(self):
        self.request
        if self.request.GET.get("show_all"):
            return Library.objects.all()
        else:
            return Library.objects.all[:5]
