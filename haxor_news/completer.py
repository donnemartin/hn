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

from __future__ import unicode_literals
from __future__ import print_function

from prompt_toolkit.completion import Completer

from .completions import SUBCOMMANDS, ARGS_OPTS_LOOKUP


class Completer(Completer):
    """Completer for haxor-news.

    :type text_utils: :class:`utils.TextUtils`
    :param text_utils: An instance of `utils.TextUtils`.

    :type fuzzy_match: bool
    :param fuzzy_match: Determines whether to use fuzzy matching.
    """

    def __init__(self, fuzzy_match, text_utils):
        self.fuzzy_match = fuzzy_match
        self.text_utils = text_utils

    def completing_command(self, words, word_before_cursor):
        """Determine if we are currently completing the hn command.

        :type words: list
        :param words: The input text broken into word tokens.

        :type word_before_cursor: str
        :param word_before_cursor: The current word before the cursor,
            which might be one or more blank spaces.

        :rtype: bool
        :return: Specifies whether we are currently completing the hn command.
        """
        if len(words) == 1 and word_before_cursor != '':
            return True
        else:
            return False

    def completing_subcommand(self, words, word_before_cursor):
        """Determine if we are currently completing a subcommand.

        :type words: list
        :param words: The input text broken into word tokens.

        :type word_before_cursor: str
        :param word_before_cursor: The current word before the cursor,
            which might be one or more blank spaces.

        :rtype: bool
        :return: Specifies whether we are currently completing a subcommand.
        """
        if (len(words) == 1 and word_before_cursor == '') \
                or (len(words) == 2 and word_before_cursor != ''):
            return True
        else:
            return False

    def completing_arg(self, words, word_before_cursor):
        """Determine if we are currently completing an arg.

        :type words: list
        :param words: The input text broken into word tokens.

        :type word_before_cursor: str
        :param word_before_cursor: The current word before the cursor,
            which might be one or more blank spaces.

        :rtype: bool
        :return: Specifies whether we are currently completing an arg.
        """
        if (len(words) == 2 and word_before_cursor == '') \
                or (len(words) == 3 and word_before_cursor != ''):
            return True
        else:
            return False

    def completing_subcommand_option(self, words, word_before_cursor):
        """Determine if we are currently completing an option.

        :type words: list
        :param words: The input text broken into word tokens.

        :type word_before_cursor: str
        :param word_before_cursor: The current word before the cursor,
            which might be one or more blank spaces.

        :rtype: list
        :return: A list of options.
        """
        options = []
        for subcommand, args_opts in ARGS_OPTS_LOOKUP.items():
            if subcommand in words and \
                (words[-2] == subcommand or
                    self.completing_subcommand_option_util(subcommand, words)):
                options.extend(ARGS_OPTS_LOOKUP[subcommand]['opts'])
        return options

    def completing_subcommand_option_util(self, option, words):
        """Determine if we are currently completing an option.

        Called by completing_subcommand_option as a utility method.

        :type option: str
        :param option: The subcommand in the elements of ARGS_OPTS_LOOKUP.

        :type words: list
        :param words: The input text broken into word tokens.

        :rtype: bool
        :return: Specifies whether we are currently completing an option.
        """
        # Example: Return True for: hn view 0 --comm
        if len(words) > 3:
            if option in words:
                return True
        return False

    def arg_completions(self, words, word_before_cursor):
        """Generates arguments completions based on the input.

        :type words: list
        :param words: The input text broken into word tokens.

        :type word_before_cursor: str
        :param word_before_cursor: The current word before the cursor,
            which might be one or more blank spaces.

        :rtype: list
        :return: A list of completions.
        """
        if 'hn' not in words:
            return []
        input_subcommand = words[1]
        if input_subcommand in ARGS_OPTS_LOOKUP:
            return [ARGS_OPTS_LOOKUP[input_subcommand]['args']]
        if input_subcommand in SUBCOMMANDS:
            return ['10']
        return []

    def get_completions(self, document, _):
        """Get completions for the current scope.

        :type document: :class:`prompt_toolkit.Document`
        :param document: An instance of `prompt_toolkit.Document`.

        :type _: :class:`prompt_toolkit.completion.Completion`
        :param _: (Unused).

        :rtype: generator
        :return: Yields an instance of `prompt_toolkit.completion.Completion`.
        """
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        words = self.text_utils.get_tokens(document.text)
        commands = []
        if len(words) == 0:
            return commands
        if self.completing_command(words, word_before_cursor):
            commands = ['hn']
        else:
            if 'hn' not in words:
                return commands
            if self.completing_subcommand(words, word_before_cursor):
                commands = list(SUBCOMMANDS.keys())
            else:
                if self.completing_arg(words, word_before_cursor):
                    commands = self.arg_completions(words, word_before_cursor)
                else:
                    commands = self.completing_subcommand_option(
                        words,
                        word_before_cursor)
        completions = self.text_utils.find_matches(
            word_before_cursor, commands, fuzzy=self.fuzzy_match)
        return completions
