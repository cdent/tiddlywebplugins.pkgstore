"""
Use package resources of a package as a place to store
tiddlers etc.
"""

try:    
        from pkg_resources import resource_filename
except ImportError:
        from tiddlywebplugins.utils import resource_filename

from tiddlyweb.stores.text import Store as TextStore

class Store(TextStore):
    """
    A store which keeps entities inside a package.
    """

    def __init__(self, store_config=None, environ=None):
        package = store_config['package']
        self.read_only = store_config.get('read_only', True)
        store_root_base = resource_filename(package, 'resources')
        store_config['store_root'] = '%s/store' % store_root_base
        super(Store, self).__init__(store_config, environ)

    def _init_store(self):
        if self.read_only:
            return
        super(Store, self)._init_store()


def init(config):
    pass
