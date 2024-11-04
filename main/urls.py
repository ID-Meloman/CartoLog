from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .views import (popular, form_newmodel, CarDetail, CarDelete, CarUpdate, filter_cars, favorites,
                    get_models_by_brand, registration_user_form, login_user, info_user, comparison_view)

urlpatterns = [
    path('', popular, name='popular_page'),
    path('favorites/', favorites, name='favorites_page'),  # Обратите внимание на добавление слэша в конце
    path('newmodel/', form_newmodel, name='newmodel_page'),  # Также добавьте слэш в конце для консистентности
    path('<int:pk>/', CarDetail.as_view(), name='car_detail'),  # Добавьте слэш в конце
    path('<int:pk>/update/', CarUpdate.as_view(), name='car_update'),  # Добавьте слэш в конце
    path('<int:pk>/delete/', CarDelete.as_view(), name='car_delete'),  # Добавьте слэш в конце
    path('filter-cars/', filter_cars, name='filter_cars'),
    path('toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('popular/', popular, name='popular'),
    path('get_models_by_brand/', get_models_by_brand, name='get_models_by_brand'),
    path('registration/', registration_user_form, name='registration_user'),
    path('login/', login_user, name='login_user'),
    path('user/', info_user, name='info_user'),
    path('get_models_by_brand/', get_models_by_brand, name='get_models_by_brand'),
    path('filter-cars/', views.filter_cars, name='filter_cars'),
    path('logout/', views.logout_user, name='logout_user'),
    path('comparison/', comparison_view, name='comparison_page'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
