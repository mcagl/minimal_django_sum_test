import datetime
from decimal import Decimal
from django.db.models import Sum
from django.test import TestCase
from my_app import models as app_models


class SumTest(TestCase):
    def setUp(self):
        self.t0 = app_models.Tag.objects.create(name="Tag0")
        self.t1 = app_models.Tag.objects.create(name="Tag1")
        self.t2 = app_models.Tag.objects.create(name="Tag2")
        self.t3 = app_models.Tag.objects.create(name="Tag3")
        # One with no tags
        app_models.Row.objects.create(
            day=datetime.date(2014, 1, 1),
            amount=Decimal('10.00'),
        )
        # One tagged Tag0
        r = app_models.Row.objects.create(
            day=datetime.date(2014, 1, 2),
            amount=Decimal('10.00'),
        )
        r.tags.add(self.t0)
        # One tagged Tag1
        r = app_models.Row.objects.create(
            day=datetime.date(2014, 1, 3),
            amount=Decimal('10.00'),
        )
        r.tags.add(self.t1)
        # One tagged Tag0, Tag1
        r = app_models.Row.objects.create(
            day=datetime.date(2014, 1, 4),
            amount=Decimal('10.00'),
        )
        r.tags.add(self.t0, self.t1)
        # One tagged Tag2, Tag3
        r = app_models.Row.objects.create(
            day=datetime.date(2014, 1, 5),
            amount=Decimal('10.00'),
        )
        r.tags.add(self.t2, self.t3)

    def test_rows_and_tags(self):
        self.assertEqual(app_models.Tag.objects.count(), 4)
        self.assertEqual(app_models.Row.objects.count(), 5)

    def test_sum(self):
        # Filter for Row objects with tags in [Tag0, Tag1], and add distinct()
        rows = app_models.Row.objects.filter(tags__in=[self.t0, self.t1]).distinct()
        # Assert that we get a queryset with 3 Row objects
        self.assertEqual(rows.count(), 3)
        # Use Sum() to sum the amount of these 3 Row objects, each with amount=10.
        # Do we get 30?
        self.assertEqual(rows.aggregate(Sum('amount'))['amount__sum'], 30)
