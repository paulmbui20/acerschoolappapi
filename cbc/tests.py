from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from django.db.utils import IntegrityError
from cbc.models import LearningArea, LearningLevel
from cbc.serializers import LearningAreaSerializer, LearningLevelsSerializer


class TestHelperMixin:
    def get_response_data(self, response):
        """Handle both paginated and non-paginated responses"""
        if isinstance(response.data, dict) and 'results' in response.data:
            return response.data['results']
        return response.data


class LearningAreaModelTests(TestCase):
    def test_learning_area_str(self):
        obj = LearningArea.objects.create(name="Mathematics", code="MATH")
        self.assertEqual(str(obj), "Mathematics")

    def test_learning_area_unique_name_case_insensitive(self):
        LearningArea.objects.create(name="English", code="ENG")
        with self.assertRaises(IntegrityError):
            LearningArea.objects.create(name="english", code="ENG2")

    def test_learning_area_unique_code(self):
        LearningArea.objects.create(name="Science", code="SCI")
        with self.assertRaises(IntegrityError):
            LearningArea.objects.create(name="Science2", code="SCI")


class LearningLevelsModelTests(TestCase):
    def test_learning_levels_str(self):
        obj = LearningLevel.objects.create(name="Grade 1")
        self.assertEqual(str(obj), "Grade 1")

    def test_unique_name_case_insensitive(self):
        LearningLevel.objects.create(name="Grade 2")
        with self.assertRaises(IntegrityError):
            LearningLevel.objects.create(name="grade 2")


class LearningAreaSerializerTests(TestCase):
    def test_serializer_output(self):
        obj = LearningArea.objects.create(name="Kiswahili", code="KIS")
        data = LearningAreaSerializer(obj).data
        self.assertEqual(data["name"], "Kiswahili")
        self.assertEqual(data["code"], "KIS")


class LearningLevelsSerializerTests(TestCase):
    def test_serializer_output(self):
        obj = LearningLevel.objects.create(name="Grade 5")
        data = LearningLevelsSerializer(obj).data
        self.assertEqual(data["name"], "Grade 5")


class LearningAreaListAPITests(TestCase, TestHelperMixin):
    def setUp(self):
        cache.clear()
        LearningArea.objects.create(name="English", code="ENG")
        LearningArea.objects.create(name="Mathematics", code="MATH")

    def test_list_endpoint_status(self):
        url = reverse("learningarea-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_list_returns_all_items(self):
        url = reverse("learningarea-list")
        res = self.client.get(url)
        data = self.get_response_data(res)
        self.assertEqual(len(data), 2)

    def test_ordering_case_insensitive(self):
        LearningArea.objects.create(name="biology", code="BIO")
        url = reverse("learningarea-list")
        res = self.client.get(url)
        data = self.get_response_data(res)
        names = [i["name"] for i in data]
        self.assertEqual(names, sorted(names, key=str.lower))

    def test_list_is_cached(self):
        url = reverse("learningarea-list")

        res1 = self.client.get(url)
        cache_key = "learningarea_list"
        cached = cache.get(cache_key)
        self.assertIsNotNone(cached)

        res2 = self.client.get(url)
        self.assertEqual(res1.data, res2.data)

    def test_cache_invalidates_on_change(self):
        url = reverse("learningarea-list")
        self.client.get(url)
        self.assertIsNotNone(cache.get("learningarea_list"))

        LearningArea.objects.create(name="New Area", code="NEW")
        self.assertIsNone(cache.get("learningarea_list"))


class LearningLevelsListAPITests(TestCase, TestHelperMixin):
    def setUp(self):
        cache.clear()
        LearningLevel.objects.create(name="Grade 1")
        LearningLevel.objects.create(name="Grade 2")

    def test_list_endpoint(self):
        url = reverse("learninglevels-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = self.get_response_data(res)
        self.assertEqual(len(data), 2)

    def test_cache_invalidates(self):
        url = reverse("learninglevels-list")
        self.client.get(url)
        self.assertIsNotNone(cache.get("learninglevels_list"))

        LearningLevel.objects.create(name="Grade 3")
        self.assertIsNone(cache.get("learninglevels_list"))


class LearningAreaDetailTests(TestCase):
    def setUp(self):
        cache.clear()
        self.obj = LearningArea.objects.create(name="English", code="ENG")

    def test_detail_status(self):
        url = reverse("learningarea-detail", args=[self.obj.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_detail_returns_correct_data(self):
        url = reverse("learningarea-detail", args=[self.obj.id])
        res = self.client.get(url)
        self.assertEqual(res.data["name"], "English")

    def test_detail_cache_created(self):
        url = reverse("learningarea-detail", args=[self.obj.id])
        self.client.get(url)
        key = f"learningarea_detail_{self.obj.id}"
        self.assertIsNotNone(cache.get(key))

    def test_detail_cache_invalidated(self):
        url = reverse("learningarea-detail", args=[self.obj.id])
        self.client.get(url)
        key = f"learningarea_detail_{self.obj.id}"
        self.assertIsNotNone(cache.get(key))

        self.obj.name = "English Updated"
        self.obj.save()

        self.assertIsNone(cache.get(key))

    def test_detail_404(self):
        url = reverse("learningarea-detail", args=[9999])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)


class LearningLevelDetailTests(TestCase):
    def setUp(self):
        cache.clear()
        self.obj = LearningLevel.objects.create(name="Grade 3")

    def test_detail(self):
        url = reverse("learninglevels-detail", args=[self.obj.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_cache_invalidation(self):
        url = reverse("learninglevels-detail", args=[self.obj.id])
        self.client.get(url)

        key = f"learninglevel_detail_{self.obj.id}"  # Fixed: should be 'learninglevel' not 'learninglevels'
        self.assertIsNotNone(cache.get(key))

        self.obj.name = "Grade 3 Updated"
        self.obj.save()

        self.assertIsNone(cache.get(key))


class RateLimitTests(TestCase):
    def test_rate_limiting_on_list(self):
        url = reverse("learningarea-list")

        for _ in range(60):
            self.client.get(url)

        res = self.client.get(url)
        self.assertEqual(res.status_code, 429)


class PaginationTests(TestCase, TestHelperMixin):
    def setUp(self):
        for i in range(30):
            LearningArea.objects.create(name=f"Area {i}", code=f"C{i}")

    def test_page_size(self):
        url = reverse("learningarea-list")
        res = self.client.get(url, {"page_size": 5})

        # Check if response is paginated
        if 'results' in res.data:
            self.assertEqual(len(res.data["results"]), 5)
        else:
            # If not paginated, check the data directly
            data = self.get_response_data(res)
            self.assertEqual(len(data), 5)
