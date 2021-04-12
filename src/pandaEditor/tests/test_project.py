import logging
import os
import shutil
import stat
import tempfile
import unittest


logger = logging.getLogger(__name__)


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(Test, cls).setUpClass()

        # Create working directory.
        cls.temp_dir_path = tempfile.mkdtemp()
        logger.info('Created working directory: {}'.format(cls.temp_dir_path))

    @classmethod
    def tearDownClass(cls):
        super(Test, cls).tearDownClass()

        # Delete working directory.
        def del_rw(action, name, exc):
            os.chmod(name, stat.S_IWRITE)
            os.remove(name)

        shutil.rmtree(cls.temp_dir_path, onerror=del_rw)
        logger.info('Deleted working directory: {}'.format(cls.temp_dir_path))
