
import os
import shutil
import py.test
from tiddlyweb.config import config

from tiddlyweb.store import Store

from tiddlyweb.store import StoreMethodNotImplemented, StoreError
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler


def setup_module(module):
    try:
        shutil.rmtree('testpackage/resources/store')
    except:  # not there
        pass
    environ = {'tiddlyweb.config': config}
    wstore = Store('tiddlywebplugins.pkgstore',
            {'package': 'testpackage', 'read_only': False},
            environ)
    module.wstore = wstore
    rstore = Store('tiddlywebplugins.pkgstore',
            {'package': 'testpackage', 'read_only': True},
            environ)
    module.rstore = rstore


def test_base_structure():
    assert os.path.exists('testpackage/resources/store')
    assert os.path.isdir('testpackage/resources/store')
    assert os.path.exists('testpackage/resources/store/recipes')
    assert os.path.isdir('testpackage/resources/store/recipes')
    assert os.path.exists('testpackage/resources/store/bags')
    assert os.path.isdir('testpackage/resources/store/bags')
    assert os.path.exists('testpackage/resources/store/users')
    assert os.path.isdir('testpackage/resources/store/users')


def test_put_bag():
    bag = Bag('testone')
    wstore.put(bag)
    assert os.path.exists('testpackage/resources/store/bags/testone')
    assert os.path.isdir('testpackage/resources/store/bags/testone')


def test_put_tiddler():
    tiddler = Tiddler('tiddlerone', 'testone')
    tiddler.text = 'oh hi'
    wstore.put(tiddler)
    assert os.path.exists(
            'testpackage/resources/store/bags/testone/tiddlers/tiddlerone')
    assert os.path.isdir(
            'testpackage/resources/store/bags/testone/tiddlers/tiddlerone')
    with open(
            'testpackage/resources/store/bags/testone/tiddlers/tiddlerone/1') as tiddler_file:
        content = tiddler_file.read().split('\n\n')[1].strip()
        assert content == 'oh hi'


def test_get_tiddler():
    tiddler = Tiddler('tiddlerone', 'testone')
    tiddler = wstore.get(tiddler)
    assert tiddler.text == 'oh hi'

    tiddler = rstore.get(tiddler)
    assert tiddler.text == 'oh hi'

    py.test.raises(StoreMethodNotImplemented, 'rstore.put(tiddler)')
    py.test.raises(StoreMethodNotImplemented, 'rstore.delete(tiddler)')

    wstore.delete(tiddler)
    py.test.raises(StoreError, 'rstore.get(tiddler)')
