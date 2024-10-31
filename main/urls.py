from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import popular, form_newcar, form_newmodel, CarDetail, CarDelete, CarUpdate

urlpatterns = [
    path('', popular, name='popular_page'),
    path('newcar', form_newcar, name='newcar_page'),
    path('newmodel', form_newmodel, name='newmodel_page'),
    path('<int:pk>', CarDetail.as_view(), name='car_detail'),
    path('<int:pk>/update', CarUpdate.as_view(), name='car_update'),
    path('<int:pk>/delete', CarDelete.as_view(), name='car_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
