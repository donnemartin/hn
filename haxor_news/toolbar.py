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
from pygments.token import Token
from prompt_toolkit.formatted_text import PygmentsTokens


class Toolbar(object):
    """Show information about the aws-shell in a tool bar.

    :type handler: callable
    :param handler: Wraps the callable `get_toolbar_items`.
    """

    def __init__(self, paginate_comments_cfg):
        self.handler = self._create_toolbar_handler(paginate_comments_cfg)

    def _create_toolbar_handler(self, paginate_comments_cfg):
        """Create the toolbar handler.

        :type paginate_comments_cfg: callable
        :param paginate_comments_cfg: Specifies whether to paginate comments.

        :rtype: callable
        :returns: get_toolbar_items.
        """
        assert callable(paginate_comments_cfg)

        def get_toolbar_items():
            """Return the toolbar items.

            :type _: :class:`prompt_toolkit.Cli`
            :param _: (Unused)

            :rtype: list
            :return: A list of (pygments.Token.Toolbar, str).
            """
            # if paginate_comments_cfg():
            #     paginate_comments_token = Token.Toolbar.On
            #     paginate_comments = 'ON'
            # else:
            #     paginate_comments_token = Token.Toolbar.Off
            #     paginate_comments = 'OFF'
            return PygmentsTokens([
                # (paginate_comments_token,
                #  ' [F2] Paginate Comments: {0} '.format(paginate_comments)),
                (Token.Toolbar, ' [F10] Exit ')
            ])

        return get_toolbar_items
