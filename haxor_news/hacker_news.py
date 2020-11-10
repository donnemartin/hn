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

import platform
import re
import sys
import webbrowser

import click
from .compat import HTMLParser
from .compat import urlparse

from .config import Config
from .lib.haxor.haxor import HackerNewsApi, HTTPError, InvalidItemID, \
    InvalidUserID
from .lib.pretty_date_time import pretty_date_time
from .onions import onions
from .web_viewer import WebViewer


class HackerNews(object):
    """Encapsulate Hacker News.

        :type COMMENT_INDENT: str (const)
        :param COMMENT_INDENT: The comment indent.

        :type COMMENT_UNSEEN: str (const)
        :param COMMENT_UNSEEN: The adornment for unseen
            comments.

        :type config: :class:`config.Config`
        :param config: An instance of `config.Config`.

        :type html: :class:`HTMLParser`
        :param html: An instance of `HTMLParser`.

        :type MAX_LIST_INDEX: int (const)
        :param MAX_LIST_INDEX: The maximum 1-based index value
            hn view will use to match item_ids.  Any value larger than
            MAX_LIST_INDEX will result in hn view treating that index as an
            actual post id.

        :type MAX_SNIPPET_LENGTH: int (const)
        :param MAX_SNIPPET_LENGTH: The max length of a comment snippet shown
            when filtering comments.

        :type hacker_news_api: :class:`haxor.HackerNewsApi`
        :param hacker_news_api: An instance of `haxor.HackerNewsApi`.

        :type QUERY_UNSEEN: str (const)
        :param foo: the query to show unseen comments.

        :type web_viewer: :class:`web_viewer.WebViewer`
        :param web_viewer: An instance of `web_viewer.WebViewer`.
    """

    COMMENT_INDENT = '  '
    COMMENT_UNSEEN = ' [!]'
    MAX_LIST_INDEX = 1000
    MAX_SNIPPET_LENGTH = 60
    QUERY_UNSEEN = '\[!\]'

    def __init__(self):
        self.hacker_news_api = HackerNewsApi()
        try:
            self.html = HTMLParser.HTMLParser()
        except:
            self.html = HTMLParser
        self.config = Config()
        self.web_viewer = WebViewer()

    def ask(self, limit):
        """Display Ask HN posts.

        :type limit: int
        :param limit: the number of items to show, optional, defaults to 10.
        """
        self.print_items(
            message=self.headlines_message('Ask HN'),
            item_ids=self.hacker_news_api.ask_stories(limit))

    def best(self, limit):
        """Display best posts.

        :type limit: int
        :param limit: the number of items to show, optional, defaults to 10.
        """
        self.print_items(
            message=self.headlines_message('Best'),
            item_ids=self.hacker_news_api.best_stories(limit))

    def headlines_message(self, message):
        """Create the "Fetching [message] Headlines..." string.

        :type message: str
        :param message: The headline message.

        :rtype: str
        :return: "Fetching [message] Headlines...".
        """
        return 'Fetching {0} Headlines...'.format(message)

    def hiring_and_freelance(self, regex_query, post_id):
        """Display comments matching the monthly who is hiring post.

        Searches the monthly Hacker News who is hiring post for comments
        matching the given regex_query.  Defaults to searching the latest
        post based on your installed version of haxor-news.

        :type regex_query: str
        :param regex_query: The regex query to match.

        :type post_id: int
        :param post_id: the who is hiring post id.
                Optional, defaults to the latest post based on your installed
                version of haxor-news.
        """
        try:
            item = self.hacker_news_api.get_item(post_id)
            self.print_comments(item,
                                regex_query,
                                comments_hide_non_matching=True)
            self.config.save_cache()
        except InvalidItemID:
            self.print_item_not_found(post_id)
        except IOError:
            sys.stderr.close()

    def jobs(self, limit):
        """Display job posts.

        :type limit: int
        :param limit: the number of items to show, optional, defaults to 10.
        """
        self.print_items(
            message=self.headlines_message('Jobs'),
            item_ids=self.hacker_news_api.job_stories(limit))

    def new(self, limit):
        """Display the latest posts.

        :type limit: int
        :param limit: the number of items to show, optional, defaults to 10.
        """
        self.print_items(
            message=self.headlines_message('Latest'),
            item_ids=self.hacker_news_api.new_stories(limit))

    def onion(self, limit):
        """Display onions.

        :type limit: int
        :param limit: the number of items to show, optional, defaults to 10.
        """
        click.secho('\n{h}\n'.format(h=self.headlines_message('Top Onion')),
                    fg=self.config.clr_title)
        index = 1
        for onion in onions[0:limit]:
            formatted_index_title = self.format_index_title(index, onion)
            click.echo(formatted_index_title)
            index += 1
        click.echo('')

    def print_comment(self, item, regex_query='',
                      comments_hide_non_matching=False, depth=0):
        """Print the comments for the given item.

        :type item: :class:`haxor.Item`
        :param item: An instance of `haxor.Item`.

        :type regex_query: str
        :param regex_query: the regex query to match.

        :type comments_hide_non_matching: bool
        :param comments_hide_non_matching: determines whether to
                hide comments that don't match (False) or truncate them (True).

        :type depth: int
        :param depth: The current recursion depth, used to indent the comment.
        """
        if item.text is None:
            return
        header_color = 'yellow'
        header_color_highlight = 'magenta'
        header_adornment = ''
        if self.config.item_cache is not None and \
                str(item.item_id) not in self.config.item_cache:
            header_adornment = self.COMMENT_UNSEEN
            self.config.item_cache.append(item.item_id)
        show_comment = True
        if regex_query is not None:
            if self.match_comment_unseen(regex_query, header_adornment) or \
                    self.match_regex(item, regex_query):
                header_color = header_color_highlight
            else:
                show_comment = False
        formatted_heading, formatted_comment = self.format_comment(
            item, depth, header_color, header_adornment)
        if show_comment:
            click.echo(formatted_heading, color=True)
            click.echo(formatted_comment, color=True)
        elif comments_hide_non_matching:
            click.secho('.', nl=False)
        else:
            click.echo(formatted_heading, color=True)
            num_chars = len(formatted_comment)
            if num_chars > self.MAX_SNIPPET_LENGTH:
                num_chars = self.MAX_SNIPPET_LENGTH
            click.echo(formatted_comment[0:num_chars] + ' [...]', color=True)

    def print_comments(self, item, regex_query='',
                       comments_hide_non_matching=False, depth=0):
        """Recursively print comments and subcomments for the given item.

        :type item: :class:`haxor.Item`
        :param item: An instance of `haxor.Item`.

        :type regex_query: str
        :param regex_query: the regex query to match.

        :type comments_hide_non_matching: bool
        :param comments_hide_non_matching: determines whether to
                hide comments that don't match (False) or truncate them (True).

        :type depth: int
        :param depth: The current recursion depth, used to indent the comment.
        """
        self.print_comment(item, regex_query, comments_hide_non_matching, depth)
        comment_ids = item.kids
        if not comment_ids:
            return
        for comment_id in comment_ids:
            try:
                comment = self.hacker_news_api.get_item(comment_id)
                depth += 1
                self.print_comments(
                    comment,
                    regex_query=regex_query,
                    comments_hide_non_matching=comments_hide_non_matching,
                    depth=depth)
                depth -= 1
            except (InvalidItemID, HTTPError):
                click.echo('')
                self.print_item_not_found(comment_id)

    def format_comment(self, item, depth, header_color, header_adornment):
        """Format a given item's comment.

        :type item: :class:`haxor.Item`
        :param item: An instance of `haxor.Item`.

        :type depth: int
        :param depth: The current recursion depth, used to indent the comment.

        :type header_color: str
        :param header_color: The header color.

        :type header_adornment: str
        :param header_adornment: The header adornment.

        :rtype: tuple
        :return: * A string representing the formatted comment header.
                 * A string representing the formatted comment.
        """
        indent = self.COMMENT_INDENT * depth
        formatted_heading = click.style(
            '\n{i}{b} - {d}{h}'.format(
                i=indent,
                b=item.by,
                d=str(pretty_date_time(item.submission_time)),
                h=header_adornment),
            fg=header_color)
        unescaped_text = self.html.unescape(item.text)
        regex_paragraph = re.compile(r'<p>')
        unescaped_text = regex_paragraph.sub(click.style(
            '\n\n' + indent), unescaped_text)
        regex_url = re.compile(r'(<a href=(".*") .*</a>)')
        unescaped_text = regex_url.sub(click.style(
            r'\2', fg=self.config.clr_link), unescaped_text)
        regex_tag = re.compile(r'(<(.*)>.*?<\/\2>)')
        unescaped_text = regex_tag.sub(click.style(
            r'\1', fg=self.config.clr_tag), unescaped_text)
        formatted_comment = click.wrap_text(text=unescaped_text,
                                            initial_indent=indent,
                                            subsequent_indent=indent)
        return formatted_heading, formatted_comment

    def format_index_title(self, index, title):
        """Format and item's index and title.

        :type index: int
        :param index: The index for the given item, used with the
            hn view [index] commend.

        :type title: str
        :param title: The item's title.

        :rtype: str
        :return: The formatted index and title.
        """
        INDEX_PAD = 5
        formatted_index = '  ' + (str(index) + '.').ljust(INDEX_PAD)
        formatted_index_title = click.style(formatted_index,
                                            fg=self.config.clr_view_index)
        formatted_index_title += click.style(title + ' ',
                                             fg=self.config.clr_title)
        return formatted_index_title

    def format_item(self, item, index):
        """Format an item.

        :type item: :class:`haxor.Item`
        :param item: An instance of `haxor.Item`.

        :type index: int
        :param index: The index for the given item, used with the
            hn view [index] commend.

        :rtype: str
        :return: The formatted item.
        """
        formatted_item = self.format_index_title(index, item.title)
        if item.url is not None:
            netloc = urlparse(item.url).netloc
            netloc = re.sub('www.', '', netloc)
            formatted_item += click.style('(' + netloc + ')',
                                          fg=self.config.clr_view_link)
        formatted_item += '\n         '
        formatted_item += click.style(str(item.score) + ' points ',
                                      fg=self.config.clr_num_points)
        formatted_item += click.style('by ' + item.by + ' ',
                                      fg=self.config.clr_user)
        submission_time = str(pretty_date_time(item.submission_time))
        formatted_item += click.style(submission_time + ' ',
                                      fg=self.config.clr_time)
        num_comments = str(item.descendants) if item.descendants else '0'
        formatted_item += click.style('| ' + num_comments + ' comments',
                                      fg=self.config.clr_num_comments)
        return formatted_item

    def print_item_not_found(self, item_id):
        """Print a message the given item id was not found.

        :type item_id: int
        :param item_id: The item's id.
        """
        click.secho('Item with id {0} not found.'.format(item_id), fg='red')

    def print_items(self, message, item_ids):
        """Print the items.

        :type message: str
        :param message: A message to print out to the user before outputting
                the results.

        :type item_ids: iterable
        :param item_ids: A collection of items to print.
                Can be a list or dictionary.
        """
        self.config.item_ids = []
        index = 1
        for item_id in item_ids:
            try:
                item = self.hacker_news_api.get_item(item_id)
                if item.title:
                    formatted_item = self.format_item(item, index)
                    self.config.item_ids.append(item.item_id)
                    click.echo(formatted_item)
                    index += 1
            except InvalidItemID:
                self.print_item_not_found(item_id)
        self.config.save_cache()
        if self.config.show_tip:
            click.secho(self.tip_view(str(index-1)))

    def tip_view(self, max_index):
        """Create the tip about the view command.

        :type max_index: string
        :param max_index: The index uppor bound, used with the
            hn view [index] commend.

        :rtype: str
        :return: The formatted tip.
        """
        tip = click.style('  Tip: View the page or comments for ',
                          fg=self.config.clr_tooltip)
        tip += click.style('1 through ', fg=self.config.clr_view_index)
        tip += click.style(str(max_index), fg=self.config.clr_view_index)
        tip += click.style(' with the following command:\n',
                           fg=self.config.clr_tooltip)
        tip += click.style('    hn view [#] ', fg=self.config.clr_view_index)
        tip += click.style(('optional: [-c] [-cr] [-cu] [-cq "regex"] [-ch]'
                            ' [-b] [--help]' + '\n'),
                           fg=self.config.clr_tooltip)
        return tip

    def match_comment_unseen(self, regex_query, header_adornment):
        """Determine if a comment is unseen based on the query and header.

        :type regex_query: str
        :param regex_query: The regex query to match.

        :type header_adornment: str
        :param header_adornment: The header adornment.

        :rtype: bool
        :return: Specifies if there is a match found.
        """
        if regex_query == self.QUERY_UNSEEN and \
                header_adornment == self.COMMENT_UNSEEN:
            return True
        else:
            return False

    def match_regex(self, item, regex_query):
        """Determine if there is a match with the given regex_query.

        :type item: :class:`haxor.Item`
        :param item: An instance of `haxor.Item`.

        :type regex_query: str
        :param regex_query: The regex query to match.

        :rtype: bool
        :return: Specifies if there is a match found.
        """
        match_time = re.search(
            regex_query,
            str(pretty_date_time(item.submission_time)))
        match_user = re.search(regex_query, item.by)
        match_text = re.search(regex_query, item.text)
        if not match_text and not match_user and not match_time:
            return False
        else:
            return True

    def show(self, limit):
        """Display Show HN posts.

        :type limit: int
        :param limit: the number of items to show, optional, defaults to 10.
        """
        self.config.stories_seen_count = limit
        self.config.latest_cmd = "show"
        self.print_items(
            message=self.headlines_message('Show HN'),
            item_ids=self.hacker_news_api.show_stories(limit))

    def top(self, limit):
        """Display the top posts.

        :type limit: int
        :param limit: the number of items to show, optional, defaults to 10.
        """
        self.config.stories_seen_count = limit
        self.config.latest_cmd = "top"
        self.print_items(
            message=self.headlines_message('Top'),
            item_ids=self.hacker_news_api.top_stories(limit))

    def next(self, x):
        """Display the next x top posts.

        :type x: int
        :param x: the number of items to show, optional, defaults to 10.
        """
        post_type = self.config.latest_cmd
        start = self.config.stories_seen_count
        end = self.config.stories_seen_count + x
        item_ids = self.hacker_news_api.next_x_stories(start, end, post_type)

        if len(item_ids) < 1:
            click.secho('Exceeds total stories count. Browse from first.',
                        fg='red')
            self.config.stories_seen_count = 0
        else:
            self.config.stories_seen_count = self.config.stories_seen_count + x
        self.print_items(
            message=self.headlines_message('Next x'), item_ids=item_ids)
        

    def user(self, user_id, submission_limit):
        """Display basic user info and submitted posts.

        :type user_id: str.
        :param user_id: The user'd login name.

        :type submission_limit: int
        :param submission_limit: the number of submissions to show.
                Optional, defaults to 10.
        """
        try:
            user = self.hacker_news_api.get_user(user_id)
            click.secho('\nUser Id: ', nl=False, fg=self.config.clr_general)
            click.secho(user_id, fg=self.config.clr_user)
            click.secho('Created: ', nl=False, fg=self.config.clr_general)
            click.secho(str(user.created), fg=self.config.clr_user)
            click.secho('Karma: ', nl=False, fg=self.config.clr_general)
            click.secho(str(user.karma), fg=self.config.clr_user)
            self.print_items('User submissions:',
                             user.submitted[0:submission_limit])
        except InvalidUserID:
            self.print_item_not_found(user_id)

    def view(self, index, comments_query, comments,
             comments_hide_non_matching, browser):
        """View the given index contents.

        Uses ids from ~/.haxornewsconfig stored in self.config.item_ids.
        If url is True, opens a browser with the url based on the given index.
        Else, displays the post's comments.

        :type index: int
        :param index: The index for the given item, used with the
            hn view [index] commend.

        :type comments: bool
        :param comments: Determines whether to view the comments
                or a simplified version of the post url.

        :type comments_hide_non_matching: bool
        :param comments_hide_non_matching: determines whether to
                hide comments that don't match (False) or truncate them (True).

        :type browser: bool
        :param browser: determines whether to view the url in a browser.
        """
        if self.config.item_ids is None:
            click.secho('There are no posts indexed, run a command such as '
                        'hn top first',
                        fg='red')
            return
        item_id = index
        if index < self.MAX_LIST_INDEX:
            try:
                item_id = self.config.item_ids[index-1]
            except IndexError:
                self.print_item_not_found(item_id)
                return
        try:
            item = self.hacker_news_api.get_item(item_id)
        except InvalidItemID:
            self.print_item_not_found(self.config.item_ids[index-1])
            return
        if not comments and item.url is None:
            click.secho('\nNo url associated with post.',
                        nl=False,
                        fg=self.config.clr_general)
            comments = True
        if comments:
            comments_url = ('https://news.ycombinator.com/item?id=' +
                            str(item.item_id))
            click.secho('\nFetching Comments from ' + comments_url,
                        fg=self.config.clr_general)
            if browser:
                webbrowser.open(comments_url)
            else:
                try:
                    self.print_comments(
                        item,
                        regex_query=comments_query,
                        comments_hide_non_matching=comments_hide_non_matching)
                    click.echo('')
                except IOError:
                    sys.stderr.close()
                self.config.save_cache()
        else:
            click.secho('\nOpening ' + item.url + ' ...',
                        fg=self.config.clr_general)
            if browser:
                webbrowser.open(item.url)
            else:
                contents = self.web_viewer.generate_url_contents(item.url)
                header = click.style('Viewing ' + item.url + '\n\n',
                                     fg=self.config.clr_general)
                contents = header + contents
                contents += click.style(('\nView this article in a browser with'
                                         ' the -b/--browser flag.\n'),
                                        fg=self.config.clr_general)
                contents += click.style(('\nPress q to quit viewing this '
                                         'article.\n'),
                                        fg=self.config.clr_general)
                if platform.system() == 'Windows':
                    try:
                        # Strip out Unicode, which seems to have issues on
                        # Windows
                        contents = re.sub(r'[^\x00-\x7F]+', '', contents)
                        click.echo(contents)
                    except IOError:
                        sys.stderr.close()
                else:
                    click.echo_via_pager(contents)
            click.echo('')

    def view_setup(self, index, comments_regex_query, comments,
                   comments_recent, comments_unseen,
                   comments_hide_non_matching, clear_cache, browser):
        """Set up the call to view the given index comments or url.

        This method is meant to be called after a command that outputs a
        table of posts.

        :type index: int
        :param index: The index for the given item, used with the
            hn view [index] commend.

        :type regex_query: str
        :param regex_query: The regex query to match.

        :type comments: bool
        :param comments: Determines whether to view the comments
                or a simplified version of the post url.

        :type comments_recent: bool
        :param comments_recent: Determines whether to view only
                recently comments (posted within the past 59 minutes or less).

        :type comments_unseen: bool
        :param comments_unseen: Determines whether to view only
                comments that you have not yet seen.

        :type comments_hide_non_matching: bool
        :param comments_hide_non_matching: determines whether to
                hide comments that don't match (False) or truncate them (True).

        :type clear_cache: bool
        :param clear_cache: foos.

        :type browser: bool
        :param browser: Determines whether to clear the comment cache before
            running the view command.
        """
        if comments_regex_query is not None:
            comments = True
        if comments_recent:
            comments_regex_query = 'seconds ago|minutes ago'
            comments = True
        if comments_unseen:
            comments_regex_query = self.QUERY_UNSEEN
            comments = True
        if clear_cache:
            self.config.clear_item_cache()
        self.view(int(index),
                  comments_regex_query,
                  comments,
                  comments_hide_non_matching,
                  browser)
