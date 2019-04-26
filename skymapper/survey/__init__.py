import os, numpy as np
from .. import register_survey, with_metaclass, with_metaclass

class BaseSurvey(object):
    def contains(self, ra, dec):
        """Whether ra, dec are inside the survey footprint"""
        if not hasattr(ra, '__iter__'):
            ra = (ra,)
        return np.zeros(len(ra), dtype='bool')

# [blatant copy from six to avoid dependency]
# python 2 and 3 compatible metaclasses
# see http://python-future.org/compatible_idioms.html#metaclasses

class Meta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)

        # remove those that are directly derived from BaseProjection
        if BaseSurvey not in bases:
            register_survey(cls)

        return cls

class Survey(with_metaclass(Meta, BaseSurvey)):
    pass

class DES(Survey):
    def __init__(self):
        import pymangle
        # get survey polygon data
        this_dir, this_filename = os.path.split(__file__)
        self.m = pymangle.Mangle(os.path.join(this_dir, "des-round17-poly_tidy.ply"))

    def contains(self, ra, dec):
        return self.m.contains(ra, dec)
