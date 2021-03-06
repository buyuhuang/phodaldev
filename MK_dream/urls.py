from __future__ import unicode_literals

from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from homepage import views as homepage_view
from feed import view as feed_view
from amp import views as amp_views
from sitemaps import views as sitemap
from sitemaps.mobile_sitemaps import DisplayableSitemap as DisplayableMobileSitemap
from sitemaps.sitemaps import DisplayableSitemap
from rest_framework_jwt.views import verify_jwt_token, obtain_jwt_token, refresh_jwt_token

admin.autodiscover()

urlpatterns = i18n_patterns(
  url("^admin/", include(admin.site.urls)),
)

sitemaps = {"sitemaps": {"all": DisplayableSitemap}}
mobile_sitemaps = {"sitemaps": {"all": DisplayableMobileSitemap}}

urlpatterns += [
  url("^sitemap\.xml$", sitemap.sitemap, sitemaps),
  url("^sitemap_mobile\.xml$", sitemap.mobile, sitemaps),
]

urlpatterns += [
  url("feeds/(?P<format>.*)/$", feed_view.blog_post_feed, name="blog_post_feed"),
  url("^blog/feeds/(?P<format>.*)/$", feed_view.blog_post_feed, name="blog_post_feed")
]

urlpatterns += [
  url("^events/", include("events.urls")),
]

urlpatterns += [
  url("^$", homepage_view.homepage, name="home"),
  url("^amp/(?P<slug>.*)/$", amp_views.amp_blog_post_detail, name="blog_post_detail"),
  url(r'^api/app/', include("api.urls")),
  url(r'^api-token-auth/', obtain_jwt_token),
  url(r'^api-token-refresh/', refresh_jwt_token),
  url(r'^api-token-verify/', verify_jwt_token),
  url("^", include("mezzanine.urls")),
]

handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
