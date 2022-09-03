# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.contrib.postgres.indexes import GinIndex, BTreeIndex
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext as _

from hitcount.models import HitCountMixin
from hitcount.settings import MODEL_HITCOUNT

from FunctionModule.accounts.models import User


class Post(models.Model, HitCountMixin):
    class Meta:
        verbose_name = "Tin bài"
        verbose_name_plural = "Tin bài"
        indexes = (
            # Full text search index
            GinIndex(fields=["title", "content"]),
            # Search for code with like
            BTreeIndex(fields=['title']),
            # Search using IN query
            BTreeIndex(fields=['title', 'content']),
        )
        #ordering = ["state", "district"]

    user = models.ForeignKey(User,  on_delete=models.RESTRICT, blank=True, null=True, verbose_name=_("Người đăng tin"))
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_published = models.BooleanField(default=True, verbose_name=_("CHO PHÉP ĐĂNG"))
    date = models.DateField(default=datetime.now, verbose_name=_("Thời gian đăng"))
    hit_count_generic = GenericRelation(
        MODEL_HITCOUNT, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return "Tiêu đề bài viết: %s" % self.title
