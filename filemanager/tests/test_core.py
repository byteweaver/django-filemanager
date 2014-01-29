from django.test import TestCase

from filemanager.core import Filemanager


class FilemanagerTest(TestCase):
    def setUp(self):
        self.fm = Filemanager()

    def test_basic_path(self):
        self.assertEqual(self.fm.path, '')
        self.assertEqual(self.fm.abspath, 'uploads')

    def test_different_path(self):
        self.fm.update_path('another/folder/')
        self.assertEqual(self.fm.path, 'another/folder')
        self.assertEqual(self.fm.abspath, 'uploads/another/folder')

    def test_path_from_root(self):
        self.fm.update_path('/folder/')
        self.assertEqual(self.fm.path, 'folder')
        self.assertEqual(self.fm.abspath, 'uploads/folder')

    def test_get_breadcrumbs(self):
        self.assertEqual([{'label': 'Filemanager', 'path': ''}], self.fm.get_breadcrumbs())
