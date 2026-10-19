#!/usr/bin/env python3
"""Regression tests for English prose, portable links, and offline validation."""
import pathlib
import tempfile
import unittest
from unittest import mock
import validate_skill as validator


class DocumentChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.page = self.root / 'SKILL.md'

    def check(self, text):
        self.page.write_text(text, encoding='utf-8')
        return validator.check_document(self.page, self.root)

    def test_unicode_data_is_allowed(self):
        self.assertEqual(self.check('# Encoding\n\n```lua\nlocal text = "工厂"\n```\n'), [])

    def test_untranslated_prose_is_rejected(self):
        self.assertTrue(self.check('# 中文标题\n'))

    def test_valid_reference(self):
        (self.root / 'topic.md').write_text('# Topic\n')
        self.assertEqual(self.check('[Topic](topic.md)\n'), [])

    def test_missing_reference(self):
        self.assertTrue(self.check('[Topic](missing.md)\n'))

    def test_archive_escape_is_rejected(self):
        self.assertTrue(self.check('[History](../archive.md)\n'))

    def test_encoded_escape_is_rejected(self):
        self.assertTrue(self.check('[History](%2e%2e/archive.md)\n'))

    def test_external_link(self):
        self.assertEqual(self.check('[Docs](https://tweaked.cc/)\n'), [])

    def test_unbalanced_fence(self):
        self.assertTrue(self.check('```lua\nlocal x = 1\n'))

    def test_offline_cache_miss_never_requests_network(self):
        with mock.patch.object(validator, 'CACHE', self.root), mock.patch.object(validator.urllib.request, 'urlopen') as request:
            with self.assertRaisesRegex(SystemExit, 'offline cache miss'):
                validator.fetch('missing.html', offline=True)
            request.assert_not_called()

    def test_offline_cache_hit(self):
        (self.root / 'cached.html').write_text('cached', encoding='utf-8')
        with mock.patch.object(validator, 'CACHE', self.root):
            self.assertEqual(validator.fetch('cached.html', offline=True), 'cached')


if __name__ == '__main__':
    unittest.main()
