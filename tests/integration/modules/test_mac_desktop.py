# -*- coding: utf-8 -*-
"""
Integration tests for the mac_desktop execution module.
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest
from salt.ext import six
from tests.support.case import ModuleCase


@pytest.mark.destructive_test
@pytest.mark.skip_if_not_root
@pytest.mark.skip_unless_on_darwin
class MacDesktopTestCase(ModuleCase):
    """
    Integration tests for the mac_desktop module.
    """

    @pytest.mark.slow_test(seconds=1)  # Test takes >0.1 and <=1 seconds
    def test_get_output_volume(self):
        """
        Tests the return of get_output_volume.
        """
        ret = self.run_function("desktop.get_output_volume")
        self.assertIsNotNone(ret)

    @pytest.mark.slow_test(seconds=5)  # Test takes >1 and <=5 seconds
    def test_set_output_volume(self):
        """
        Tests the return of set_output_volume.
        """
        current_vol = self.run_function("desktop.get_output_volume")
        to_set = 10
        if current_vol == six.text_type(to_set):
            to_set += 2
        new_vol = self.run_function(
            "desktop.set_output_volume", [six.text_type(to_set)]
        )
        check_vol = self.run_function("desktop.get_output_volume")
        self.assertEqual(new_vol, check_vol)

        # Set volume back to what it was before
        self.run_function("desktop.set_output_volume", [current_vol])

    @pytest.mark.slow_test(seconds=1)  # Test takes >0.1 and <=1 seconds
    def test_screensaver(self):
        """
        Tests the return of the screensaver function.
        """
        self.assertTrue(self.run_function("desktop.screensaver"))

    @pytest.mark.slow_test(seconds=1)  # Test takes >0.1 and <=1 seconds
    def test_lock(self):
        """
        Tests the return of the lock function.
        """
        self.assertTrue(self.run_function("desktop.lock"))

    @pytest.mark.slow_test(seconds=5)  # Test takes >1 and <=5 seconds
    def test_say(self):
        """
        Tests the return of the say function.
        """
        self.assertTrue(self.run_function("desktop.say", ["hello", "world"]))
