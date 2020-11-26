from datetime import date

from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from .models import TestGroup, TestGroupHistory


@receiver(pre_save, sender=TestGroup)
def update_test_group(sender, instance, raw, **kwargs):
    if not raw:
        try:
            if instance.deleted_at:
                return

            print('Updated')
            original = TestGroup.objects.get(pk=instance.pk)
            fm_list_id = original.failure_modes.values_list('id', flat=True)
            TestGroupHistory.objects.create(test_group=original,
                                            start_date=original.start_date,
                                            failure_modes=','.join(
                                                [str(i) for i in fm_list_id]),
                                            created_at=date.today(),
                                            event=TestGroupHistory.Actions.UPDATED,
                                            tests=original.tests)
        except:
            return


@receiver(post_save, sender=TestGroup)
def create_test_group(sender, instance, created, **kwargs):
    if created:
        TestGroupHistory.objects.create(test_group=instance,
                                        start_date=instance.start_date,
                                        failure_modes='',
                                        created_at=date.today(),
                                        event=TestGroupHistory.Actions.CREATED,
                                        tests=instance.tests)


@receiver(post_save, sender=TestGroup)
def delete_test_group(sender, instance, created, **kwargs):
    if instance.deleted_at:
        fm_list_id = instance.failure_modes.values_list('id', flat=True)
        TestGroupHistory.objects.create(test_group=instance,
                                        start_date=instance.start_date,
                                        failure_modes=','.join(
                                            [str(i) for i in fm_list_id]),
                                        created_at=date.today(),
                                        event=TestGroupHistory.Actions.DELETED,
                                        tests=instance.tests)
