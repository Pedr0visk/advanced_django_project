import csv
import time
import concurrent.futures

from collections import defaultdict
from io import StringIO

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

from apps.cuts.models import Cut
from apps.failuremodes.models import FailureMode


def get_column(row, index):
    """
    if column is blank return 1
    """
    if row[index] is None or row[index] == '':
        return 1
    else:
        return row[index]


class Loader:
    """
    This class is in charge of saving multiples records on database
    """

    def __init__(self, filepath, safety_function):
        self.filepath = filepath
        self.cuts = []
        self.sf = safety_function

    def run(self):
        file = self.filepath.read().decode('utf-8')
        infile = csv.reader(StringIO(file), delimiter='\n')
        rows = [line[0].split(',') for line in infile][1:]

        bulk_mgr = BulkCreateManager(chunk_size=100)

        for row in rows:
            index = row[0]
            fm_list = row[1:]
            bulk_mgr.add(Cut(index=index,
                             order=len(fm_list),
                             failure_modes=','.join(fm_list),
                             safety_function=self.sf))

        bulk_mgr.done()

        return True

class BulkCreateManager(object):
    """
    This helper class keeps track of ORM objects to be created for multiple
    model classes, and automatically creates those objects with `bulk_create`
    when the number of objects accumulated for a given model class exceeds
    `chunk_size`.
    Upon completion of the loop that's `add()`ing objects, the developer must
    call `done()` to ensure the final set of objects is created for all models.
    """

    def __init__(self, chunk_size=100):
        self._create_queues = defaultdict(list)
        self.chunk_size = chunk_size

    def _commit(self, model_class):
        model_key = model_class._meta.label
        model_class.objects.bulk_create(self._create_queues[model_key], ignore_conflicts=True)
        self._create_queues[model_key] = []

    def add(self, obj):
        """
        Add an object to the queue to be created, and call bulk_create if we
        have enough objs.
        """
        model_class = type(obj)
        model_key = model_class._meta.label
        self._create_queues[model_key].append(obj)
        if len(self._create_queues[model_key]) >= self.chunk_size:
            self._commit(model_class)

    def done(self):
        """
        Always call this upon completion to make sure the final partial chunk
        is saved.
        """
        for model_name, objs in self._create_queues.items():
            if len(objs) > 0:
                self._commit(apps.get_model(model_name))
