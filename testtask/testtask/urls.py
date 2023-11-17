"""
URL configuration for testtask project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views

Add an import:  from my_app import views
Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views

Add an import:  from other_app.views import Home
Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf

Import the include() function: from django.urls import include, path
Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from myapp.views import QueryView, ResultView, PingView, HistoryView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="MyApp API",
        default_version='v1',
        description="API for handling queries and results",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('query/<str:cadastre_number>/', QueryView.as_view(), name='query'),
    path('result/<int:query_id>/', ResultView.as_view(), name='result'),
    path('ping/', PingView.as_view(), name='ping'),
    path('history/', HistoryView.as_view(), name='history'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]