from django.contrib import admin
from django.urls import path , include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from django.contrib.auth import views
# from django.contrib.auth.views import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('', include('accounts.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path(r'^accounts/login/$', login, {'template_name': 'admin/login.html'}),
    # path(r'^accounts/logout/$', logout),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



