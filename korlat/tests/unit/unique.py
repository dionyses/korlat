import re
from threading import Thread
import unittest

from korlat.common.unique import identifier, fqdn, email


class RequestIdentifiers(Thread):
    def __init__(self, n_requests):
        super(RequestIdentifiers, self).__init__()
        self.unique_identifiers = []
        self.n_requests = n_requests

    def run(self):
        while len(self.unique_identifiers) < self.n_requests:
            self.unique_identifiers += [identifier()]


class Tests(unittest.TestCase):
    def setUp(self):
        pass

    def test_unique_identifier(self):
        a = identifier()
        b = identifier()
        self.assertIsNotNone(re.match("\d{6}-\d{6}-\d{4}$", a))
        self.assertIsNotNone(re.match("\d{6}-\d{6}-\d{4}$", b))
        self.assertNotEqual(a, b)
        self.assertIsNotNone(re.match("asdf-\d{6}-\d{6}-\d{4}$", identifier("asdf")))

    def test_unique_fqdn(self):
        a = fqdn()
        b = fqdn()
        self.assertIsNotNone(re.match("\w{3,}\.\w{3,}\.\w{3,}$", a))
        self.assertIsNotNone(re.match("\w{3,}\.\w{3,}\.\w{3,}$", b))
        self.assertNotEqual(a, b)

    def test_unique_email(self):
        a = email()
        b = email()
        self.assertIsNotNone(re.match("\w{3,}@\w{3,}\.\w{3,}$", a))
        self.assertIsNotNone(re.match("\w{3,}@\w{3,}\.\w{3,}$", b))
        self.assertNotEqual(a, b)

    def test_unique_across_threads(self):
        tries = 1000
        r1 = RequestIdentifiers(tries)
        r2 = RequestIdentifiers(tries)
        r3 = RequestIdentifiers(tries)
        r1.start()
        r2.start()
        r3.start()

        while r1.is_alive() or r2.is_alive() or r3.is_alive():
            pass

        self.assertEqual(len(r1.unique_identifiers), tries)
        self.assertEqual(len(r2.unique_identifiers), tries)
        self.assertEqual(len(r1.unique_identifiers), tries)

        s1 = set(r1.unique_identifiers)
        s2 = set(r2.unique_identifiers)
        s3 = set(r3.unique_identifiers)

        self.assertEqual(len(s1), tries)
        self.assertEqual(len(s2), tries)
        self.assertEqual(len(s3), tries)
        accumulate_set = s1.union(s2).union(s3)
        self.assertEqual(len(accumulate_set), tries * 3)


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)

