import csv
from collections import defaultdict
from django.apps import apps

from apps.subsystems.models import Subsystem
from apps.components.models import Component
from apps.failuremodes.models import FailureMode


class Loader:
    """
    This class is in charge of saving multiples records on database
    """

    def __init__(self, filepath, bop):
        self.filepath = filepath
        self.subsystems = []
        self.components = []
        self.failuremodes = []
        self.tests = []
        self.bop = bop
        self.row = []

    def run(self):
        with open(self.filepath) as csvfile:
            # read file from line 1
            infile = csv.reader(csvfile, delimiter=',')
            rows = [line for line in infile][1:]

            for row in rows:
                self.row = row
                # add subsystem to bulk
                s, created = Subsystem.objects.get_or_create(code=row[2],
                                                             name=row[1],
                                                             bop=self.bop)

                # add component to bulk
                c, created = Component.objects.get_or_create(code=row[4],
                                                             name=row[3],
                                                             subsystem=s)

                # add failure mode to bulk
                FailureMode.objects.get_or_create(code=row[6],
                                                  name=row[5],
                                                  distribution=self.get_distribution_attr(row),
                                                  diagnostic_coverage=self.get_column(row, 17),
                                                  component=c)

    def get_distribution_attr(self, row):
        """"""
        distribution = {'type': row[22]}

        if row[22] == 'Exponential':
            distribution['exponential_failure_rate'] = row[23]

        elif row[22] == 'Probability':
            distribution['probability'] = self.get_column(row, 23)

        elif row[22] == 'Weibull':
            distribution['scale'] = row[24]
            distribution['form'] = row[25]

        elif row[22] == 'Step':
            distribution['cycle'] = {}
            distribution['initial_failure_rate'] = row[26]
            distribution['cycle']['value'] = int(row[27]) / 100
            distribution['cycle']['limit'] = row[28]
            distribution['cycle']['size'] = row[29]

        return distribution

    @staticmethod
    def get_column(row, index):
        """
        if column is blank return 1
        """
        if row[index] is None or row[index] == '':
            return 1
        else:
            return row[index]


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
