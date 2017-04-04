import abc
import sys


class BaseLoader(object):
    __metclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        sys.meta_path.append(self)
