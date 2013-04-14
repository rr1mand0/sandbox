from django.conf.urls import patterns, include, url

from crust.polls import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$/', views.index, name='index')
  )
