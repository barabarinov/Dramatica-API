from rest_framework.pagination import PageNumberPagination


class ReservationPagination(PageNumberPagination):
    page_size = 10
