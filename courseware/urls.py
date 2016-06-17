from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.hello, name='home'),
    url(r'block/(?P<usage_id>.+)/(?P<handler_slug>.+)?/', views.block_handler, name='block_handler'),
    url(r'course/(?P<usage_id>.+)', views.course_student_view),
]
