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

import click

from .hacker_news import HackerNews


pass_hacker_news = click.make_pass_decorator(HackerNews)


class HackerNewsCli(object):
    """Encapsulate the Hacker News Command Line Interface."""

    @click.group()
    @click.pass_context
    def cli(ctx):
        """Main entry point for HackerNewsCli.

        :type ctx: :class:`click.core.Context`
        :param ctx: An instance of click.core.Context that stores an instance
            of `hacker_news.HackerNews`.
        """
        # Create a HackerNews object and remember it as the context object.
        # From this point onwards other commands can refer to it by using the
        # @pass_hacker_news decorator.
        ctx.obj = HackerNews()

    @cli.command()
    @click.argument('limit', required=False, default=10)
    @pass_hacker_news
    def ask(hacker_news, limit):
        """Display Ask HN posts.

        Example(s):
            hn ask
            hn ask 5

        :type hacker_news: :class:`hacker_news.HackerNews`
        :param hacker_news: An instance of `hacker_news.HackerNews`.

        :type limit: int
        :param limit: specifies the number of items to show.
            Optional, defaults to 10.
        """
        hacker_news.ask(limit)

    @cli.command()
    @click.argument('limit', required=False, default=10)
    @pass_hacker_news
    def best(hacker_news, limit):
        """Display the best posts of the past few days.

        Example(s):
            hn best
            hn best 20

        :type hacker_news: :class:`hacker_news.HackerNews`
        :param hacker_news: An instance of `hacker_news.HackerNews`.

        :type limit: int
        :param limit: specifies the number of items to show.
            Optional, defaults to 10.
        """
        hacker_news.best(limit)

    @cli.command()
    @click.argument('regex_query', required=False)
    @click.option('-i', '--id_post', required=False, default=0)
    @pass_hacker_news
    def freelance(hacker_news, regex_query, id_post):
        """Display comments from the seeking freelancer posts.

        Searches the monthly Hacker News seeking freelancer post for comments
        matching the given regex_query.  Defaults to searching the latest
        post.

        You can search any post by providing a freelancer_post_id:
            Example: https://news.ycombinator.com/item?id=10492087
            freelancer_post_id = 10492087

        Example(s):
            hn freelance
            hn freelance "Python"
            hn freelance "(?i)Python|JavaScript"  # (?i) case insensitive
            hn freelance "(?i)Python" -i 8394339  # search post 8394339
            hn freelance "(?i)(Python|JavaScript).*(rockstar)" > rockstars.txt

        :type hacker_news: :class:`hacker_news.HackerNews`
        :param hacker_news: An instance of `hacker_news.HackerNews`.

        :type regex_query: str
        :param regex_query: The regex query to match.

        :type id_post: str
        :param id_post: The who is hiring post id.
                Optional, defaults to the latest post based on your installed
                version of haxor-news.
        """
        if id_post == 0:
            hacker_news.config.load_hiring_and_freelance_ids()
            id_post = hacker_news.config.freelance_id
        hacker_news.hiring_and_freelance(regex_query, id_post)

    @cli.command()
    @click.argument('regex_query', required=False)
    @click.option('-i', '--id_post', required=False, default=0)
    @pass_hacker_news
    def hiring(hacker_news, regex_query, id_post):
        """Display comments from the who is hiring posts.

        Searches the monthly Hacker News who is hiring post for comments
        matching the given regex_query.  Defaults to searching the latest
        post.

        You can search any post by providing a who_is_hiring_post_id:
            Example: https://news.ycombinator.com/item?id=10492086
            who_is_hiring_post_id = 10492086

        Example(s):
            hn hiring
            hn hiring "Python"
            hn hiring "(?i)Python|JavaScript"  # (?i) case insensitive
            hn hiring "(?i)Python|JavaScript" -i 8394339  # search post 8394339
            hn hiring "(?i)(Python|JavaScript).*(rockstar)" > rockstars.txt

        :type hacker_news: :class:`hacker_news.HackerNews`
        :param hacker_news: An instance of `hacker_news.HackerNews`.

        :type regex_query: str
        :param regex_query: The regex query to match.

        :type id_post: str
        :param id_post: The who is hiring post id.
                Optional, defaults to the latest post based on your installed
                version of haxor-news.
        """
        if id_post == 0:
            hacker_news.config.load_hiring_and_freelance_ids()
            id_post = hacker_news.config.hiring_id
        hacker_news.hiring_and_freelance(regex_query, id_post)

    @cli.command()
    @click.argument('limit', required=False, default=10)
    @pass_hacker_news
    def jobs(hacker_news, limit):
        """Display job posts.

        Example(s):
            hn jobs
            hn jobs 15

        :type hacker_news: :class:`hacker_news.HackerNews`
        :param hacker_news: An instance of `hacker_news.HackerNews`.

        :type limit: int
        :param limit: specifies the number of items to show.
            Optional, defaults to 10.
        """
        hacker_news.jobs(limit)

    @cli.command()
    @click.argument('limit', required=False, default=10)
    @pass_hacker_news
    def new(hacker_news, limit):
        """Display the latest posts.

        Example(s):
            hn new
            hn new 20

        :type hacker_news: :class:`hacker_news.HackerNews`
        :param hacker_news: An instance of `hacker_news.HackerNews`.

        :type limit: int
        :param limit: specifies the number of items to show.
            Optional, defaults to 10.
        """
        hacker_news.new(limit)

    @cli.command()
    @click.argument('limit', required=False, default=50)
    @pass_hacker_news
    def onion(hacker_news, limit):
        """Display onions.

        Example(s):
            hn onion
            hn onion 10

        :type hacker_news: :class:`hacker_news.HackerNews`
        :param hacker_news: An instance of `hacker_news.HackerNews`.

        :type limit: int
        :param limit: specifies the number of items to show.
            Optional, defaults to 10.
        """
        hacker_news.onion(limit)

    @cli.command()
    @click.argument('limit', required=False, default=10)
    @pass_hacker_news
    def show(hacker_news, limit):
        """Display Show HN posts.

        Example(s):
            hn show
            hn show 5

        :type hacker_news: :class:`hacker_news.HackerNews`
        :param hacker_news: An instance of `hacker_news.HackerNews`.

        :type limit: int
        :param limit: specifies the number of items to show.
            Optional, defaults to 10.
        """
        hacker_news.show(limit)

    @cli.command()
    @click.argument('limit', required=False, default=10)
    @pass_hacker_news
    def top(hacker_news, limit):
        """Display the top recent posts.

        Example(s):
            hn top
            hn top 20

        :type hacker_news: :class:`hacker_news.HackerNews`
        :param hacker_news: An instance of `hacker_news.HackerNews`.

        :type limit: int
        :param limit: specifies the number of items to show.
            Optional, defaults to 10.
        """
        hacker_news.top(limit)

    @cli.command()
    @click.argument('x', required=False, default=10)
    @pass_hacker_news
    def next(hacker_news, x):
        """Display the next x top recent posts.

        Example(s):
            hn next
            hn next 20

        :type hacker_news: :class:`hacker_news.HackerNews`
        :param hacker_news: An instance of `hacker_news.HackerNews`.

        :param limit: specifies the number of next x ranked 
                        items to show.
            Optional, defaults to 10.
        """
        hacker_news.next(x)

    @cli.command()
    @click.argument('user_id')
    @click.option('-l', '--limit', required=False, default=10)
    @pass_hacker_news
    def user(hacker_news, user_id, limit):
        """Display basic user info and submitted posts.

        Example(s):
            hn user tptacek
            hn user patio11

        :type hacker_news: :class:`hacker_news.HackerNews`
        :param hacker_news: An instance of `hacker_news.HackerNews`.

        :type user_id: str
        :param user_id: The user name/id.

        :type limit: int
        :param limit: specifies the number of items to show.
            Optional, defaults to 10.
        """
        hacker_news.user(user_id, limit)

    @cli.command()
    @click.argument('index')
    @click.option('-cq', '--comments_regex_query', required=False, default=None)
    @click.option('-c', '--comments', is_flag=True)
    @click.option('-cr', '--comments_recent', is_flag=True)
    @click.option('-cu', '--comments_unseen', is_flag=True)
    @click.option('-b', '--browser', is_flag=True)
    @click.option('-cc', '--clear_cache', is_flag=True)
    @click.option('-ch', '--comments_hide_non_matching', is_flag=True)
    @pass_hacker_news
    def view(hacker_news, index, comments_regex_query, comments,
             comments_recent, comments_unseen,
             comments_hide_non_matching, clear_cache, browser):
        """View the post index or id, hn view --help.

        Example(s):
            hn top
            hn view 3
            hn view 3 -c | less
            hn view 3 -c > comments.txt
            hn view 3 -cr
            hn view 3 --comments_recent
            hn view 3 -cu
            hn view 3 --comments_unseen
            hn view 3 -cu -ch
            hn view 3 --comments_unseen --comments_hide_non_matching
            hn view 3 --browser
            hn view 3 -b -c
            hn view 3 -comments -clear_cache
            hn view 3 "(?i)case insensitive match" --comments
            hn view 3 "(?i)programmer" --comments
            hn view 3 "(?i)programmer" --comments | less
            hn view 10492086
            hn view 10492086 "Python"
            hn view 10492086 "(?i)case insensitive match"
            hn view 10492086 "(?i)(Python|Django)" > comments.txt

        :type hacker_news: :class:`hacker_news.HackerNews`
        :param hacker_news: An instance of `hacker_news.HackerNews`.

        :type index: str
        :param index: specifies either:
                1) the index of a post just shown within a list of posts or
                2) the actual post id
            For example, calling `hn top` will list the top posts with
            1-based indices for each post:
                1. Post foo
                2. Post bar
                3. Post baz
            A subsequent call to `hn view 1` will view 'Post foo'.
            Providing an index larger than MAX_LIST_INDEX (1000) will
            result in hn view treating index as an actual post id.

        :type comments_regex_query: :class:`x.y`
        :param comments_regex_query: the regex query to match.
        Passing this option automatically sets comments to True.

        :type comments: bool
        :param comments: Determines whether to view the comments
                or a simplified version of the post url.

        :type comments_recent: bool
        :param comments_recent: Determines whether to view only
                recently comments (posted within the past 59 minutes or less).

        :type comments_unseen: bool
        :param comments_unseen: determines whether to view only
                comments that you have not yet seen.

        :type comments_hide_non_matching: bool
        :param comments_hide_non_matching: determines whether to
                hide comments that don't match (False) or truncate them (True).

        :type clear_cache: bool
        :param clear_cache: Determines whether to clear the comment cache before
                running the view command.

        :type browser: bool
        :param browser: Determines whether to view the url
                in a browser.
        """
        try:
            post_index = int(index)
        except ValueError:
            click.secho('Error: Expected an integer post index', fg='red')
        else:
            hacker_news.view_setup(post_index,
                                   comments_regex_query,
                                   comments,
                                   comments_recent,
                                   comments_unseen,
                                   comments_hide_non_matching,
                                   clear_cache,
                                   browser)
