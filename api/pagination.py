from rest_framework.pagination import PageNumberPagination
from api.models import UserProfile


class CustomPagination(PageNumberPagination):
    page_size = 12
    max_page_size = 120
    page_size_query_param = "page_size"

    def get_page_size(self, request):
        if request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=request.user)

                return user_profile.page_size
            except UserProfile.DoesNotExist:
                pass

        return super().get_page_size(request)