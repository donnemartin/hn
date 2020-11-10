# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from __future__ import print_function
from __future__ import division

import mock
from tests.compat import unittest

from click.testing import CliRunner

from haxor_news.hacker_news_cli import HackerNewsCli


class HackerNewsCliTest(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        self.hacker_news_cli = HackerNewsCli()
        self.limit = 10
        self.user = 'foo'
        self.dummy = 'foo'

    def test_cli(self):
        result = self.runner.invoke(self.hacker_news_cli.cli)
        assert result.exit_code == 0

    @mock.patch('haxor_news.hacker_news_cli.HackerNews.ask')
    def test_ask(self, mock_hn_call):
        result = self.runner.invoke(self.hacker_news_cli.cli, ['ask'])
        mock_hn_call.assert_called_with(self.limit)
        assert result.exit_code == 0

    @mock.patch('haxor_news.hacker_news_cli.HackerNews.best')
    def test_best(self, mock_hn_call):
        result = self.runner.invoke(self.hacker_news_cli.cli, ['best'])
        mock_hn_call.assert_called_with(self.limit)
        assert result.exit_code == 0

    @mock.patch('haxor_news.hacker_news_cli.HackerNews.hiring_and_freelance')
    def test_hiring(self, mock_hn_call):
        result = self.runner.invoke(
            self.hacker_news_cli.cli, ['hiring', self.dummy, '-i', 1])
        mock_hn_call.assert_called_with(self.dummy, 1)
        assert result.exit_code == 0

    @mock.patch('haxor_news.hacker_news_cli.HackerNews.hiring_and_freelance')
    def test_freelance(self, mock_hn_call):
        result = self.runner.invoke(
            self.hacker_news_cli.cli, ['freelance', self.dummy, '-i', 1])
        mock_hn_call.assert_called_with(self.dummy, 1)
        assert result.exit_code == 0

    @mock.patch('haxor_news.hacker_news_cli.HackerNews.jobs')
    def test_jobs(self, mock_hn_call):
        result = self.runner.invoke(self.hacker_news_cli.cli, ['jobs'])
        mock_hn_call.assert_called_with(self.limit)
        assert result.exit_code == 0

    @mock.patch('haxor_news.hacker_news_cli.HackerNews.new')
    def test_new(self, mock_hn_call):
        result = self.runner.invoke(self.hacker_news_cli.cli, ['new'])
        mock_hn_call.assert_called_with(self.limit)
        assert result.exit_code == 0

    @mock.patch('haxor_news.hacker_news_cli.HackerNews.onion')
    def test_onion(self, mock_hn_call):
        result = self.runner.invoke(
            self.hacker_news_cli.cli, ['onion', str(self.limit)])
        mock_hn_call.assert_called_with(self.limit)
        assert result.exit_code == 0

    @mock.patch('haxor_news.hacker_news_cli.HackerNews.show')
    def test_show(self, mock_hn_call):
        result = self.runner.invoke(self.hacker_news_cli.cli, ['show'])
        mock_hn_call.assert_called_with(self.limit)
        assert result.exit_code == 0

    @mock.patch('haxor_news.hacker_news_cli.HackerNews.top')
    def test_top(self, mock_hn_call):
        result = self.runner.invoke(self.hacker_news_cli.cli, ['top'])
        mock_hn_call.assert_called_with(self.limit)
        assert result.exit_code == 0

    @mock.patch('haxor_news.hacker_news_cli.HackerNews.next')
    def test_next(self, mock_hn_call):
        result = self.runner.invoke(self.hacker_news_cli.cli, ['next'])
        mock_hn_call.assert_called_with(self.limit)
        assert result.exit_code == 0

    @mock.patch('haxor_news.hacker_news_cli.HackerNews.user')
    def test_user(self, mock_hn_call):
        result = self.runner.invoke(
            self.hacker_news_cli.cli, ['user', self.user])
        mock_hn_call.assert_called_with(self.user, self.limit)
        assert result.exit_code == 0

    @mock.patch('haxor_news.hacker_news_cli.HackerNews.view')
    def test_view(self, mock_hn_call):
        dummy = False
        index = '0'
        result = self.runner.invoke(
            self.hacker_news_cli.cli, ['view', index])
        mock_hn_call.assert_called_with(int(index), None, dummy, dummy, dummy)
        assert result.exit_code == 0
