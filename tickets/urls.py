from django.urls import path, include
from .views import LoginView, UserListCreateView, TicketListCreateView, TicketRetrieveUpdateDestroyView, ticket_list, LogoutView, TicketViewSet

from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static 
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# router = DefaultRouter()
# router.register('files', TicketViewSet, basename='files')

urlpatterns = [
    # path('rest/', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    # path('users/', UserListCreateView.as_view(), name='users')
    path('users/', UserListCreateView, name='users'),
    # path('tickets/', TicketListCreateView.as_view(), name='ticket-list-create'),
    path('tickets/', ticket_list, name='ticket-list-create'),
    path('tickets/<int:pk>/', TicketRetrieveUpdateDestroyView.as_view(), name='ticket-retrieve-update-destroy'),
    path('logout/', LogoutView.as_view(), name='logout'),
] 

urlpatterns += staticfiles_urlpatterns()