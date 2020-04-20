# -*- coding: utf-8 -*-
"""
Tests for the salt runner

.. versionadded:: 2016.11.0
"""
from __future__ import absolute_import, print_function, unicode_literals

import pytest
from tests.support.case import ShellCase


@pytest.mark.windows_whitelisted
class SaltRunnerTest(ShellCase):
    """
    Test the salt runner
    """

    @pytest.mark.slow_test(seconds=5)  # Test takes >1 and <=5 seconds
    def test_salt_cmd(self):
        """
        test return values of salt.cmd
        """
        ret = self.run_run_plus("salt.cmd", "test.ping")
        out_ret = ret.get("out")[0]
        return_ret = ret.get("return")

        self.assertEqual(out_ret, "True")
        self.assertTrue(return_ret)

    @pytest.mark.slow_test(seconds=5)  # Test takes >1 and <=5 seconds
    def test_salt_cmd_invalid(self):
        """
        test return values of salt.cmd invalid parameters
        """
        ret = self.run_run_plus("salt.cmd")
        expected = "Passed invalid arguments:"
        self.assertIn(expected, ret["return"])
