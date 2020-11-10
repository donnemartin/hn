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
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys


class KeyManager(object):
    """A custom :class:`prompt_toolkit.KeyBindingManager`.

    Handle togging of:
        * Comment pagination.

    :type key_bindings: :class:`prompt_toolkit.key_binding.KeyBindings`
    :param key_bindings: An instance of `prompt_toolkit.key_binding.KeyBindings`
    """

    def __init__(self, set_paginate_comments, get_paginate_comments):
        self.key_bindings = None
        self._create_key_manager(set_paginate_comments, get_paginate_comments)

    def _create_key_manager(self, set_paginate_comments, get_paginate_comments):
        """Create and initialize the keybinding manager.

        :type set_paginate_comments: callable
        :param set_paginate_comments: Sets the paginate comments config.

        :type get_paginate_comments: callable
        :param get_paginate_comments: Gets the paginate comments config.

        :rtype: :class:`prompt_toolkit.key_binding.manager.
            KeyBindingManager`
        :return: An instance of `prompt_toolkit.key_binding.manager.
            KeyBindingManager`.
        """
        assert callable(set_paginate_comments)
        assert callable(get_paginate_comments)
        self.key_bindings = KeyBindings()

        @self.key_bindings.add('f2')
        def handle_f2(_):
            """Enable/Disable paginate comments mode.

            This method is currently disabled.

            :type _: :class:`prompt_toolkit.Event`
            :param _: (Unused)

            :raises: :class:`EOFError` to quit the app.
            """
            # set_paginate_comments(not get_paginate_comments())
            pass

        @self.key_bindings.add('f10')
        def handle_f10(event):
            """Quit when the `F10` key is pressed.

            :type _: :class:`prompt_toolkit.Event`
            :param _: (Unused)

            :raises: :class:`EOFError` to quit the app.
            """
            event.app.exit()

        @self.key_bindings.add('c-space')
        def handle_ctrl_space(event):
            """Initialize autocompletion at the cursor.

            If the autocompletion menu is not showing, display it with the
            appropriate completions for the context.

            If the menu is showing, select the next completion.

            :type event: :class:`prompt_toolkit.Event`
            :param event: An instance of `prompt_toolkit.Event`.
            """
            b = event.cli.current_buffer
            if b.complete_state:
                b.complete_next()
            else:
                b.start_completion(select_first=False)
