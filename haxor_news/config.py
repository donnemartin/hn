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

import os

import click
from .compat import configparser
from .compat import URLError
from .compat import urlretrieve
from .settings import freelancer_post_id, who_is_hiring_post_id


class Config(object):
    """Hacker News config.

    :type clr_x: str
    :param clr_x: Various ansi color config colors to use for highlights.

    :type CONFIG: str
    :param CONFIG: The config file name.

    :type CONFIG_SECTION: str
    :param CONFIG_SECTION: The main config file section label.

    :type CONFIG_CLR_X: str
    :param CONFIG_CLR_X: Various ansi color config labels to use for highlights.

    :type CONFIG_IDS: str
    :param CONFIG_IDS: The last list of seen post ids config label.

    :type CONFIG_CACHE: str
    :param CONFIG_CACHE: The list of seen comments config label.

    :type CONFIG_HIRING_ID: str
    :param CONFIG_HIRING_ID: The monthly freelancer post id config label.

    :type CONFIG_FREELANCE_ID: str
    :param CONFIG_FREELANCE_ID: The monthly who's hiring post id config label.

    :type CONFIG_SHOW_TIP: bool
    :param CONFIG_SHOW_TIP: determines whether to show the tip.

    :type freelance_id: int
    :param freelance_id: The monthly freelancer hiring post id.

    :type hiring_id: int
    :param hiring_id: The monthly who's hiring post id.

    :type item_cache: list
    :param item_cache: A list of seen comment ids.
            TODO: Look into an OrderedSet for improved lookup performance
            http://code.activestate.com/recipes/576694/

    :type item_ids: list
    :param item_ids: The last set of ids the user has seen,
            which allows the user to quickly access an item with the
            gh view [#] [-u/--url] command.

    :type MAX_ITEM_CACHE_SIZE: int
    :param MAX_ITEM_CACHE_SIZE: The maximum size of seen comment ids cache.
    """

    CONFIG = '.haxornewsconfig'
    CONFIG_CLR_BOLD = 'clr_bold'
    CONFIG_CLR_CODE = 'clr_code'
    CONFIG_CLR_GENERAL = 'clr_general'
    CONFIG_CLR_HEADER = 'clr_header'
    CONFIG_CLR_LINK = 'clr_link'
    CONFIG_CLR_LIST = 'clr_list'
    CONFIG_CLR_NUM_COMMENTS = 'clr_num_comments'
    CONFIG_CLR_NUM_POINTS = 'clr_num_points'
    CONFIG_CLR_TAG = 'clr_tag'
    CONFIG_CLR_TIME = 'clr_time'
    CONFIG_CLR_TITLE = 'clr_title'
    CONFIG_CLR_TOOLTIP = 'clr_tooltip'
    CONFIG_CLR_USER = 'clr_user'
    CONFIG_CLR_VIEW_LINK = 'clr_view_link'
    CONFIG_CLR_VIEW_INDEX = 'clr_view_index'
    CONFIG_SECTION = 'haxor-news'
    CONFIG_IDS = 'item_ids'
    CONFIG_CACHE = 'item_cache'
    CONFIG_HIRING_ID = 'hiring_id'
    CONFIG_FREELANCE_ID = 'freelance_id'
    CONFIG_SHOW_TIP = 'show_tip'
    MAX_ITEM_CACHE_SIZE = 20000
    CONFIG_STORIES_SEEN_COUNT = 'stories_seen_count'
    CONFIG_LATEST_CMD = 'latest_cmd'

    def __init__(self):
        self.item_ids = []
        self.item_cache = []
        self.hiring_id = 0
        self.freelance_id = 0
        self.show_tip = True
        self._init_colors()
        self.load_config([
            self.load_config_item_ids,
            self.load_config_item_cache,
            self.load_config_colors,
            self.load_config_show_tip,
            self.load_config_stories_seen_count,
            self.load_config_latest_cmd,
        ])

    def _init_colors(self):
        """Initialize colors to their defaults."""
        self.clr_bold = 'cyan'
        self.clr_code = 'cyan'
        self.clr_general = None
        self.clr_header = 'yellow'
        self.clr_link = 'green'
        self.clr_list = 'cyan'
        self.clr_num_comments = 'green'
        self.clr_num_points = 'green'
        self.clr_tag = 'cyan'
        self.clr_time = 'yellow'
        self.clr_title = None
        self.clr_tooltip = None
        self.clr_user = 'cyan'
        self.clr_view_link = 'magenta'
        self.clr_view_index = 'magenta'

    def clear_item_cache(self):
        """Clear the item cache."""
        self.item_cache = []
        self.save_cache()

    def get_config_path(self, config_file_name):
        """Get the config file path.

        :type config_file_name: str
        :param config_file_name: The config file name.

        :rtype: str
        :return: The config file path.
        """
        home = os.path.abspath(os.environ.get('HOME', ''))
        config_file_path = os.path.join(home, config_file_name)
        return config_file_path

    def load_config(self, config_funcs):
        """Load the specified config from ~/.haxornewsconfig.

        :type config_funcs: list
        :param config_funcs: The config functions to run.
        """
        config_file_path = self.get_config_path(self.CONFIG)
        parser = configparser.RawConfigParser()
        try:
            with open(config_file_path) as config_file:
                try:
                    parser.read_file(config_file)
                except AttributeError:
                    parser.readfp(config_file)
                for config_func in config_funcs:
                    config_func(parser)
        except IOError:
            # There might not be a cache yet, just silently return.
            return None

    def load_config_colors(self, parser):
        """Load the color config from ~/.haxornewsconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.
        """
        self.load_colors(parser)

    def load_config_hiring_and_freelance_ids(self, parser):
        """Load the hiring and freelance ids from ~/.haxornewsconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.
        """
        self.hiring_id = parser.getint(self.CONFIG_SECTION,
                                       self.CONFIG_HIRING_ID)
        self.freelance_id = parser.getint(self.CONFIG_SECTION,
                                          self.CONFIG_FREELANCE_ID)

    def load_config_item_cache(self, parser):
        """Load the item cache from ~/.haxornewsconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.
        """
        self.item_cache = self.load_section_list(parser,
                                                 self.CONFIG_CACHE)

    def load_config_item_ids(self, parser):
        """Load the item ids from ~/.haxornewsconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.
        """
        self.item_ids = self.load_section_list(parser,
                                               self.CONFIG_IDS)

    def load_config_stories_seen_count(self, parser):
        """Load the count stories that are already shown 
            from ~/.haxornewsconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.
        """
        self.stories_seen_count = parser.getint(self.CONFIG_SECTION, 
                                                self.CONFIG_STORIES_SEEN_COUNT)

    def load_config_latest_cmd(self, parser):
        """Load the latest command (top or show) that the user executed 
            from ~/.haxornewsconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.
        """
        self.latest_cmd = parser.get(self.CONFIG_SECTION, 
                                                self.CONFIG_LATEST_CMD)

    def load_config_show_tip(self, parser):
        """Load the show tip config from ~/.haxornewsconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.
        """
        self.show_tip = parser.getboolean(self.CONFIG_SECTION,
                                          self.CONFIG_SHOW_TIP)

    def load_color(self, parser, color_config, default):
        """Load the specified color from ~/.haxornewsconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.

        :type color_config: str
        :param color_config: The color config label to load.

        :type default: str
        :param default: The default color if no color config exists.
        """
        try:
            color = parser.get(self.CONFIG_SECTION, color_config)
            if color == 'none':
                color = None
            # Check if the user input a valid color.
            # If invalid, this will throw a TypeError
            click.style('', fg=color)
        except (TypeError, configparser.NoOptionError):
            return default
        return color

    def load_colors(self, parser):
        """Load all colors from ~/.haxornewsconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.
        """
        self.clr_bold = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_BOLD,
            default=self.clr_bold)
        self.clr_code = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_CODE,
            default=self.clr_code)
        self.clr_general = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_GENERAL,
            default=self.clr_general)
        self.clr_header = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_HEADER,
            default=self.clr_header)
        self.clr_link = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_LINK,
            default=self.clr_link)
        self.clr_list = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_LIST,
            default=self.clr_list)
        self.clr_num_comments = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_NUM_COMMENTS,
            default=self.clr_num_comments)
        self.clr_num_points = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_NUM_POINTS,
            default=self.clr_num_points)
        self.clr_tag = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_TAG,
            default=self.clr_tag)
        self.clr_time = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_TIME,
            default=self.clr_time)
        self.clr_title = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_TITLE,
            default=self.clr_title)
        self.clr_tooltip = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_TOOLTIP,
            default=self.clr_tooltip)
        self.clr_user = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_USER,
            default=self.clr_user)
        self.clr_view_link = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_VIEW_LINK,
            default=self.clr_view_link)
        self.clr_view_index = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_VIEW_INDEX,
            default=self.clr_view_index)

    def load_hiring_and_freelance_ids(self, url=None):
        """Load the latest who's hiring and freelancer post ids.

        The latest ids are updated monthly on the repo and are then cached.
        If fetching the latest ids from the repo fails, the cache is checked.
        If fetching the cache fails, the default ids set during installation
        are used.

        :type url: str
        :param url: The url to load the latest post ids.
        """
        try:
            if url is None:
                url = 'https://raw.githubusercontent.com/donnemartin/haxor-news/master/haxor_news/settings.py'  # NOQA
            file_name = 'downloaded_settings.py'
            urlretrieve(url, file_name)
            with open(file_name, 'r') as f:
                for line in f:
                    if line.startswith('who_is_hiring_post_id'):
                        self.hiring_id = line.split(' = ')[1].strip('\n')
                    if line.startswith('freelancer_post_id'):
                        self.freelance_id = line.split(' = ')[1].strip('\n')
            if self.hiring_id == 0 or self.freelance_id == 0:
                self.load_hiring_and_freelance_ids_from_cache_or_defaults()
        except (URLError, IOError):
            self.load_hiring_and_freelance_ids_from_cache_or_defaults()

    def load_hiring_and_freelance_ids_from_cache_or_defaults(self):
        """Load the hiring and freelancer post ids from cache or defaults.

        If fetching the cache fails, the default ids set during installation
        are used.
        """
        self.load_config([self.load_config_hiring_and_freelance_ids])
        if self.hiring_id == 0 or self.freelance_id == 0:
            self.hiring_id = who_is_hiring_post_id
            self.freelance_id = freelancer_post_id

    def load_section_list(self, parser, section):
        """Load the given section containing a list from ~/.haxornewsconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.

        :type section: str
        :param section: The section to load.

        :rtype: list
        :return: Collection of items stored in config.

        :raises: `Exception` if an error occurred reading from the parser.
        """
        items_ids = parser.get(self.CONFIG_SECTION, section)
        items_ids = items_ids.strip()
        excludes = ['[', ']', "'"]
        for exclude in excludes:
            items_ids = items_ids.replace(exclude, '')
        return items_ids.split(', ')

    def save_cache(self):
        """Save the current set of item ids and cache to ~/.haxornewsconfig."""
        if self.item_cache is not None and \
                len(self.item_cache) > self.MAX_ITEM_CACHE_SIZE:
            self.item_cache = self.item_cache[-self.MAX_ITEM_CACHE_SIZE//2:]
        config_file_path = self.get_config_path(self.CONFIG)
        parser = configparser.RawConfigParser()
        parser.add_section(self.CONFIG_SECTION)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_HIRING_ID,
                   self.hiring_id)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_FREELANCE_ID,
                   self.freelance_id)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_SHOW_TIP,
                   self.show_tip)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_BOLD,
                   self.clr_bold)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_CODE,
                   self.clr_code)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_GENERAL,
                   self.clr_general)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_HEADER,
                   self.clr_header)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_LINK,
                   self.clr_link)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_LIST,
                   self.clr_list)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_NUM_COMMENTS,
                   self.clr_num_comments)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_NUM_POINTS,
                   self.clr_num_points)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_TAG,
                   self.clr_tag)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_TIME,
                   self.clr_time)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_TITLE,
                   self.clr_title)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_TOOLTIP,
                   self.clr_tooltip)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_USER,
                   self.clr_user)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_VIEW_LINK,
                   self.clr_view_link)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_VIEW_INDEX,
                   self.clr_view_index)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_IDS,
                   self.item_ids)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CACHE,
                   self.item_cache)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_STORIES_SEEN_COUNT,
                   self.stories_seen_count)        
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_LATEST_CMD,
                   self.latest_cmd)
        with open(config_file_path, 'w+') as config_file:
            parser.write(config_file)
