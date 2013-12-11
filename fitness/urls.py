from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^get_foods_for_id/$', 'food.views.get_foods_for_id'),
    url(r'^get_food/$', 'food.views.get_food', name='get_food'),

    url(r'^get_all_bodyweight_numbers/$',
        'weight.views.get_all_bodyweight_numbers'),

    url(r'^admin/', include(admin.site.urls)),
)
