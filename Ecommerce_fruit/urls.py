import imp
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404,handler500


urlpatterns = [
    path('',include("store.urls")),
    path('accounts/',include("accounts.urls")),

    path('admin/', admin.site.urls),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


# handler404='page_error.views.errorpage_404'

