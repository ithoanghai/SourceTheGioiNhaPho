from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from ..blog.models import Post
from ..listings.models import Listing


class Static_Sitemap(Sitemap):

    priority = 1.0
    changefreq = 'daily'


    def items(self):
        return ['blogs', 'index', 'about','message','specialistus','specialist','whychoose','services','contacts','recruitment']

    def location(self, item):
        return reverse(item)


class Listing_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        list = []
        for listing in Listing.objects.all():
            list.append(f'/listings/{listing.id}')
        return list

    def location(self, obj):
        return obj

    # def lastmod(self, obj):
    #     return obj.date_created


class Blog_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Post.objects.all()

    def location(self, obj):
        return obj.full_path

    def lastmod(self, obj):
        return obj.date_created