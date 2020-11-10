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

from haxor_news.hacker_news import HackerNews
from tests.data.comment import formatted_comment, formatted_heading, raw_comment
from tests.data.item import formatted_items
from tests.data.markdown import formatted_markdown, raw_markdown
from tests.data.regex import raw_text_for_regex
from tests.data.tip import formatted_tip
from tests.data.title import formatted_title, raw_title
from tests.mock_hacker_news_api import MockHackerNewsApi


class HackerNewsTest(unittest.TestCase):

    def setUp(self):
        self.hn = HackerNews()
        self.hn.hacker_news_api = MockHackerNewsApi()
        self.limit = len(self.hn.hacker_news_api.items)
        self.valid_id = 0
        self.invalid_id = 9000
        self.query = 'foo'

    def top(self, limit=2):
        self.hn.print_items(
            message=self.headlines_message('Top'),
            item_ids=self.hn.hacker_news_api.top_stories(limit))

    @mock.patch('haxor_news.hacker_news.HackerNews.print_items')
    def test_ask(self, mock_print_items):
        self.hn.ask(self.limit)
        mock_print_items.assert_called_with(
            message=self.hn.headlines_message('Ask HN'),
            item_ids=self.hn.hacker_news_api.ask_stories(self.limit))

    @mock.patch('haxor_news.hacker_news.HackerNews.print_items')
    def test_best(self, mock_print_items):
        self.hn.best(self.limit)
        mock_print_items.assert_called_with(
            message=self.hn.headlines_message('Best'),
            item_ids=self.hn.hacker_news_api.best_stories(self.limit))

    def test_format_markdown(self):
        result = self.hn.web_viewer.format_markdown(raw_markdown)
        assert result == formatted_markdown

    def test_headlines_message(self):
        message = 'foo'
        headlines_message = self.hn.headlines_message(message)
        assert message in headlines_message

    @mock.patch('haxor_news.hacker_news.HackerNews.print_comments')
    @mock.patch('haxor_news.hacker_news.HackerNews.print_item_not_found')
    def test_hiring_and_freelance(self,
                                  mock_print_item_not_found,
                                  mock_print_comments):
        self.hn.hiring_and_freelance(self.query, post_id=self.valid_id)
        item = self.hn.hacker_news_api.get_item(self.valid_id)
        mock_print_comments.assert_called_with(
            item, self.query, comments_hide_non_matching=True)
        self.hn.hiring_and_freelance(self.query, post_id=self.invalid_id)
        mock_print_item_not_found.assert_called_with(self.invalid_id)

    @mock.patch('haxor_news.hacker_news.HackerNews.print_items')
    def test_jobs(self, mock_print_items):
        self.hn.jobs(self.limit)
        mock_print_items.assert_called_with(
            message=self.hn.headlines_message('Jobs'),
            item_ids=self.hn.hacker_news_api.ask_stories(self.limit))

    @mock.patch('haxor_news.hacker_news.HackerNews.print_items')
    def test_new(self, mock_print_items):
        self.hn.new(self.limit)
        mock_print_items.assert_called_with(
            message=self.hn.headlines_message('Latest'),
            item_ids=self.hn.hacker_news_api.new_stories(self.limit))

    @mock.patch('haxor_news.hacker_news.HackerNews.format_index_title')
    @mock.patch('haxor_news.hacker_news.click')
    def test_onion(self, mock_click, mock_format_index_title):
        self.hn.onion(self.limit)
        assert len(mock_format_index_title.mock_calls) == self.limit
        assert mock_click.mock_calls

    @mock.patch('haxor_news.hacker_news.HackerNews.print_items')
    def test_show(self, mock_print_items):
        self.hn.show(self.limit)
        mock_print_items.assert_called_with(
            message=self.hn.headlines_message('Show HN'),
            item_ids=self.hn.hacker_news_api.show_stories(self.limit))

    @mock.patch('haxor_news.hacker_news.HackerNews.print_items')
    def test_top(self, mock_print_items):
        self.hn.top(self.limit)
        mock_print_items.assert_called_with(
            message=self.hn.headlines_message('Top'),
            item_ids=self.hn.hacker_news_api.top_stories(self.limit))

    @mock.patch('haxor_news.hacker_news.HackerNews.print_items')
    def test_next_x_top_stories(self, mock_print_items):
        self.hn.config.stories_seen_count = 0
        self.hn.config.latest_cmd = "top"
        self.hn.next(self.limit)
        mock_print_items.assert_called_with(
            message=self.hn.headlines_message('Next x'),
            item_ids=self.hn.hacker_news_api.next_x_stories(0, self.limit, "top"))

    @mock.patch('haxor_news.hacker_news.HackerNews.print_items')
    def test_next_x_show_stories(self, mock_print_items):
        self.hn.config.stories_seen_count = 0
        self.hn.config.latest_cmd = "show"
        self.hn.next(self.limit)
        mock_print_items.assert_called_with(
            message=self.hn.headlines_message('Next x'),
            item_ids=self.hn.hacker_news_api.next_x_stories(0, self.limit, "show"))

    @mock.patch('haxor_news.hacker_news.HackerNews.print_items')
    @mock.patch('haxor_news.hacker_news.click')
    @mock.patch('haxor_news.hacker_news.HackerNews.print_item_not_found')
    def test_user(self, mock_print_item_not_found,
                  mock_click, mock_print_items):
        user_id = 'foo'
        self.hn.user(user_id, self.limit)
        user = self.hn.hacker_news_api.get_user(user_id)
        mock_print_items.assert_called_with(
            'User submissions:', user.submitted[0:self.limit])
        assert mock_click.mock_calls
        self.hn.user(self.invalid_id, self.limit)
        mock_print_item_not_found.assert_called_with(self.invalid_id)

    @mock.patch('haxor_news.hacker_news.HackerNews.view')
    def test_view_setup_query_recent(self, mock_view):
        index = 0
        comments = False
        comments_recent = True
        comments_unseen = False
        comments_hide_non_matching = False
        comments_clear_cache = False
        browser = False
        self.hn.view_setup(
            index, self.query, comments, comments_recent,
            comments_unseen, comments_hide_non_matching,
            comments_clear_cache, browser)
        comments_expected = True
        mock_view.assert_called_with(
            index, 'seconds ago|minutes ago', comments_expected,
            comments_hide_non_matching, browser)

    @mock.patch('haxor_news.hacker_news.HackerNews.view')
    def test_view_setup_query_unseen(self, mock_view):
        index = 0
        comments = False
        comments_recent = False
        comments_unseen = True
        comments_hide_non_matching = False
        comments_clear_cache = False
        browser = False
        self.hn.view_setup(
            index, self.query, comments, comments_recent,
            comments_unseen, comments_hide_non_matching,
            comments_clear_cache, browser)
        comments_expected = True
        mock_view.assert_called_with(
            index, self.hn.QUERY_UNSEEN, comments_expected,
            comments_hide_non_matching, browser)

    def test_format_comment(self):
        item = self.hn.hacker_news_api.get_item(self.valid_id)
        item.text = raw_comment
        heading, comment = self.hn.format_comment(
            item, depth=3, header_color='yellow', header_adornment='')
        assert heading == formatted_heading
        assert comment == formatted_comment

    def test_format_index_title(self):
        result = self.hn.format_index_title(
            index=1, title=raw_title)
        assert result == formatted_title

    def test_format_item(self):
        items = self.hn.hacker_news_api.items
        for index, item in enumerate(items):
            result = self.hn.format_item(items[index], index+1)
            assert result == formatted_items[index]

    @mock.patch('haxor_news.hacker_news.click.echo')
    def test_print_comments_unseen(self, mock_click_echo):
        items = self.hn.hacker_news_api.items
        self.hn.print_comments(items[0],
                               regex_query=self.hn.QUERY_UNSEEN)
        mock_click_echo.assert_any_call(
            '\x1b[35m\nfoo - just now [!]\x1b[0m', color=True)
        mock_click_echo.assert_any_call(
            'text foo', color=True)
        mock_click_echo.assert_any_call(
            '\x1b[35m\n  bar - just now [!]\x1b[0m', color=True)
        mock_click_echo.assert_any_call(
            '  text bar', color=True)
        mock_click_echo.assert_any_call(
            '\x1b[35m\n    baz - just now [!]\x1b[0m', color=True)
        mock_click_echo.assert_any_call(
            '    text baz', color=True)

    @mock.patch('haxor_news.hacker_news.click.echo')
    @mock.patch('haxor_news.hacker_news.click.secho')
    def test_print_comments_unseen_hide_non_matching(self,
                                                     mock_click_secho,
                                                     mock_click_echo):
        items = self.hn.hacker_news_api.items
        self.hn.config.item_cache.extend(['0', '1', '2'])
        self.hn.print_comments(items[0],
                               regex_query=self.hn.QUERY_UNSEEN,
                               comments_hide_non_matching=True)
        mock_click_secho.assert_any_call('.', nl=False)
        assert mock_click_secho.mock_calls
        assert not mock_click_echo.mock_calls

    @mock.patch('haxor_news.hacker_news.click.echo')
    def test_print_comments_regex(self, mock_click_echo):
        items = self.hn.hacker_news_api.items
        regex_query = 'foo'
        self.hn.print_comments(items[0], regex_query)
        mock_click_echo.assert_any_call(
            '\x1b[35m\nfoo - just now [!]\x1b[0m', color=True)
        mock_click_echo.assert_any_call(
            'text foo', color=True)
        mock_click_echo.assert_any_call(
            '\x1b[33m\n  bar - just now [!]\x1b[0m', color=True)
        mock_click_echo.assert_any_call(
            '  text bar [...]', color=True)
        mock_click_echo.assert_any_call(
            '\x1b[33m\n    baz - just now [!]\x1b[0m', color=True)
        mock_click_echo.assert_any_call(
            '    text baz [...]', color=True)

    @mock.patch('haxor_news.hacker_news.click.echo')
    def test_print_comments_regex_hide_non_matching(self, mock_click_echo):
        items = self.hn.hacker_news_api.items
        regex_query = 'foo'
        self.hn.print_comments(items[0],
                               regex_query,
                               comments_hide_non_matching=True)
        mock_click_echo.assert_any_call(
            '\x1b[35m\nfoo - just now [!]\x1b[0m', color=True)
        mock_click_echo.assert_any_call(
            'text foo', color=True)

    @mock.patch('haxor_news.hacker_news.click.echo')
    def test_print_comments_regex_seen(self, mock_click_echo):
        items = self.hn.hacker_news_api.items
        item = items[2]
        regex_query = 'foo'
        self.hn.config.item_cache.append(str(item.item_id))
        self.hn.print_comments(item, regex_query)
        mock_click_echo.assert_any_call(
            '\x1b[33m\nbaz - just now\x1b[0m', color=True)
        mock_click_echo.assert_any_call(
            'text baz [...]', color=True)

    @mock.patch('haxor_news.hacker_news.click')
    def test_print_item_not_found(self, mock_click):
        self.hn.print_item_not_found(self.invalid_id)
        mock_click.secho.assert_called_with(
            'Item with id {0} not found.'.format(self.invalid_id), fg='red')

    @mock.patch('haxor_news.hacker_news.click')
    @mock.patch('haxor_news.hacker_news.HackerNews.format_item')
    def test_print_items(self, mock_format_item, mock_click):
        items = self.hn.hacker_news_api.items
        item_ids = [item.item_id for item in items]
        self.hn.print_items(self.hn.headlines_message(
            'Top'), item_ids)
        for index, item in enumerate(items):
            assert mock.call(item, index+1) in mock_format_item.mock_calls
        assert mock_click.secho.mock_calls

    def test_print_tip_view(self):
        result = self.hn.tip_view(max_index=10)
        assert result == formatted_tip

    def test_match_comment_unseen(self):
        regex_query = ''
        header_adornment = ''
        match = self.hn.match_comment_unseen(regex_query, header_adornment)
        assert not match
        regex_query = self.hn.QUERY_UNSEEN
        header_adornment = self.hn.COMMENT_UNSEEN
        match = self.hn.match_comment_unseen(regex_query, header_adornment)
        assert match

    def test_match_regex(self):
        regex_query = '(?i)(Python|JavaScript).*(rockstar)'
        item = self.hn.hacker_news_api.get_item(self.valid_id)
        assert not self.hn.match_regex(item, regex_query)
        item.text = raw_text_for_regex
        assert self.hn.match_regex(item, regex_query)

    def test_match_regex_user(self):
        regex_query = 'bar'
        item = self.hn.hacker_news_api.get_item(self.valid_id)
        assert not self.hn.match_regex(item, regex_query)
        regex_query = 'fo'
        assert self.hn.match_regex(item, regex_query)

    def test_match_regex_item(self):
        regex_query = 'just now'
        item = self.hn.hacker_news_api.get_item(self.valid_id)
        assert self.hn.match_regex(item, regex_query)
        regex_query = 'minutes ago'
        assert not self.hn.match_regex(item, regex_query)

    @mock.patch('haxor_news.hacker_news.WebViewer.generate_url_contents')
    @mock.patch('haxor_news.hacker_news.click')
    def test_view(self, mock_click, mock_generate_url_contents):
        items = self.hn.hacker_news_api.items
        self.hn.config.item_ids = [int(item.item_id) for item in items]
        one_based_index = self.valid_id + 1
        comments_query = ''
        comments = False
        comments_hide_non_matching = False
        browser = False
        self.hn.view(one_based_index, comments_query, comments,
                     comments_hide_non_matching, browser)
        mock_generate_url_contents.assert_called_with(
            items[self.valid_id].url)
        assert mock_click.secho.mock_calls
        assert mock_click.echo_via_pager.mock_calls

    @mock.patch('haxor_news.hacker_news.HackerNews.print_comments')
    @mock.patch('haxor_news.hacker_news.click')
    def test_view_comments(self, mock_click, mock_print_comments):
        items = self.hn.hacker_news_api.items
        self.hn.config.item_ids = [int(item.item_id) for item in items]
        one_based_index = self.valid_id + 1
        comments_query = 'foo'
        comments = True
        comments_hide_non_matching = False
        browser = False
        self.hn.view(one_based_index, comments_query, comments,
                     comments_hide_non_matching, browser)
        mock_print_comments.assert_called_with(
            items[self.valid_id],
            comments_hide_non_matching=False,
            regex_query=comments_query)
        assert mock_click.mock_calls

    @mock.patch('haxor_news.hacker_news.HackerNews.print_comments')
    @mock.patch('haxor_news.hacker_news.click')
    def test_view_no_url(self, mock_click, mock_print_comments):
        self.hn.hacker_news_api.items[0].url = None
        items = self.hn.hacker_news_api.items
        self.hn.config.item_ids = [int(item.item_id) for item in items]
        one_based_index = self.valid_id + 1
        comments_query = 'foo'
        comments = False
        comments_hide_non_matching = False
        browser = False
        self.hn.view(one_based_index, comments_query, comments,
                     comments_hide_non_matching, browser)
        mock_print_comments.assert_called_with(
            items[self.valid_id],
            comments_hide_non_matching=False,
            regex_query=comments_query)
        assert mock_click.mock_calls

    @mock.patch('haxor_news.hacker_news.webbrowser')
    @mock.patch('haxor_news.hacker_news.click')
    def test_view_browser_url(self, mock_click, mock_webbrowser):
        items = self.hn.hacker_news_api.items
        self.hn.config.item_ids = [int(item.item_id) for item in items]
        one_based_index = self.valid_id + 1
        comments_query = 'foo'
        comments = False
        comments_hide_non_matching = False
        browser = True
        self.hn.view(one_based_index, comments_query, comments,
                     comments_hide_non_matching, browser)
        mock_webbrowser.open.assert_called_with(items[self.valid_id].url)
        assert mock_click.mock_calls

    @mock.patch('haxor_news.hacker_news.webbrowser')
    @mock.patch('haxor_news.hacker_news.click')
    def test_view_browser_comments(self, mock_click, mock_webbrowser):
        items = self.hn.hacker_news_api.items
        self.hn.config.item_ids = [int(item.item_id) for item in items]
        one_based_index = self.valid_id + 1
        comments_query = 'foo'
        comments = True
        comments_hide_non_matching = False
        browser = True
        self.hn.view(one_based_index, comments_query, comments,
                     comments_hide_non_matching, browser)
        item = items[self.valid_id]
        comments_url = ('https://news.ycombinator.com/item?id=' +
                        str(item.item_id))
        mock_webbrowser.open.assert_called_with(comments_url)
        assert mock_click.mock_calls
