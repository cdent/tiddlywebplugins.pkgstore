
from tiddlyweb.config import config

from tiddlyweb.store import Store

def test_create_store():
    environ = {'tiddlyweb.config': config}
    store = Store('tiddlywebplugins.pkgstore',
            {'package': 'testpackage', 'read_only': False},
            environ)
    environ['tiddlyweb.store'] = store

    print store

