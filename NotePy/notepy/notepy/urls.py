from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.splash, name='splash'),
                  path('sign_up', views.sign_up, name='sign_up'),
                  path('log_in', views.log_in, name="log_in"),
                  path('log_out', views.log_out, name="log_out"),
                  path('load_notes', views.load_notes, name="load_notes"),
                  path('create_note', views.create_note, name="create_note"),
                  path('save_note', views.save_note, name='save_note'),
                  path('close_note', views.close_note, name='close_note'),
                  path('home', views.home, name='home')
              ] + static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT)
