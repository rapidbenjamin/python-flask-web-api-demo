import sys
from peak.util.proxies import ObjectProxy, ObjectWrapper
from .base import BaseLoader


class Lazy(BaseLoader):
    def __init__(self, module_name, attrs):
        super(Lazy, self).__init__()
        self.module_name = module_name
        self.attrs = attrs
        self.active = True
        self.module = None
        self.loaded = False

    def find_module(self, full_name, path=None):
        if self.active and full_name == self.module_name:
            return self

    def load_module(self, full_name):
        if full_name in sys.modules:
            return sys.modules[full_name]

        if not self.loaded:
            self.module = self.create_lazy_module()
            self.loaded = True
        sys.modules[full_name] = self.module
        return self.module

    def create_lazy_module(self):
        attrs = self.attrs

        class LazyModule(ObjectWrapper):
            __slots__ = attrs

            def __init__(self):
                super(LazyModule, self).__init__(None)
                for attr in attrs:
                    setattr(self, attr, ObjectProxy(None))

        return LazyModule()

    def ready(self):
        self.load_module(self.module_name)  # Make sure it's been loaded.
        del sys.modules[self.module_name]
        self.active = False
        module = __import__(self.module_name, fromlist=True)
        self.active = True
        del sys.modules[self.module_name]

        self.module.__subject__ = module
        for attr in self.attrs:
            proxy = getattr(self.module, attr)
            proxy.__subject__ = getattr(module, attr)
