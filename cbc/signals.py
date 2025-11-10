from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import LearningArea, LearningLevel

LIST_CACHE_KEYS = [
    "learningarea_list",
    "learninglevels_list",
]


def detail_cache_key(model_name, obj_id):
    return f"{model_name}_detail_{obj_id}"


def invalidate_all_learning_caches(instance=None):
    # Invalidate list caches
    for key in LIST_CACHE_KEYS:
        cache.delete(key)

    # Invalidate detail cache for specific object
    if instance:
        model_name = instance.__class__.__name__.lower()
        cache.delete(detail_cache_key(model_name, instance.id))


@receiver(post_save, sender=LearningArea)
@receiver(post_delete, sender=LearningArea)
@receiver(post_save, sender=LearningLevel)
@receiver(post_delete, sender=LearningLevel)
def clear_cache_on_change(sender, instance, **kwargs):
    invalidate_all_learning_caches(instance)