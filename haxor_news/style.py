# -*- coding: utf-8

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

from pygments.token import Token
from pygments.util import ClassNotFound
from prompt_toolkit.styles.pygments import style_from_pygments_dict, style_from_pygments_cls
from prompt_toolkit.styles import merge_styles
import pygments.styles


class StyleFactory(object):
    """Provide styles for the autocomplete menu and the toolbar.

    :type style: :class:`pygments.style.StyleMeta`
    :param style: An instance of `pygments.style.StyleMeta`.
    """

    def __init__(self, name):
        self.style = self.style_factory(name)

    def style_factory(self, name):
        """Retrieve the specified pygments style.

        If the specified style is not found, the vim style is returned.

        :type style_name: str
        :param style_name: The pygments style name.

        :rtype: :class:`pygments.style.StyleMeta`
        :return: An instance of `pygments.style.StyleMeta`.
        """
        try:
            pygments_style = pygments.styles.get_style_by_name(name)
        except ClassNotFound:
            pygments_style = pygments.styles.get_style_by_name('native')

        # Create styles dictionary.
        return merge_styles([
            style_from_pygments_cls(pygments_style),
            style_from_pygments_dict({
                Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
                Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
                Token.Menu.Completions.Meta.Current: 'bg:#00aaaa #000000',
                Token.Menu.Completions.Meta: 'bg:#00aaaa #ffffff',
                Token.Menu.Completions.ProgressButton: 'bg:#003333',
                Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
                Token.Scrollbar: 'bg:#00aaaa',
                Token.Scrollbar.Button: 'bg:#003333',
                Token.Toolbar: 'bg:#222222 #cccccc',
                Token.Toolbar.Off: 'bg:#222222 #696969',
                Token.Toolbar.On: 'bg:#222222 #ffffff',
                Token.Toolbar.Search: 'noinherit bold',
                Token.Toolbar.Search.Text: 'nobold',
                Token.Toolbar.System: 'noinherit bold',
                Token.Toolbar.Arg: 'noinherit bold',
                Token.Toolbar.Arg.Text: 'nobold'
            })
        ])
