import unittest
import transaction

from pyramid import testing

from pp.common.db import dbsetup

class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        # TODO: run dbsetup.setup() with some db modules
        dbsetup.init("sqlite:///:memory:")
        with transaction.manager:
            dbsetup.create()
            # TODO: add some db things to test against

    def tearDown(self):
        testing.tearDown()

    def test_it(self):
        from pp.web.base.views import ping
        request = testing.DummyRequest()
        res = ping(request)
        # TODO: assert some results
