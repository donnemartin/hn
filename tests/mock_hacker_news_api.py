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

from haxor_news.lib.haxor.haxor import InvalidItemID, InvalidUserID


class MockItem(object):

    def __init__(self):
        self.item_id = None
        self.by = None
        self.submission_time = None
        self.text = None
        self.kids = None
        self.url = None
        self.score = None
        self.title = None
        self.descendants = None


class MockUser(object):

    def __init__(self):
        self.user_id = None
        self.created = None
        self.karma = None
        self.submitted = None


class MockHackerNewsApi(object):

    def __init__(self):
        self.items = self._generate_mock_items()
        self.users = self._generate_mock_users()

    def _generate_mock_items(self):
        items = []
        item0 = MockItem()
        item0.item_id = 0
        item0.by = 'foo'
        item0.submission_time = None
        item0.text = 'text foo'
        item0.kids = [1]
        item0.url = 'foo.com'
        item0.score = 10
        item0.title = 'title foo'
        item0.descendants = 2
        items.append(item0)
        item1 = MockItem()
        item1.item_id = 1
        item1.by = 'bar'
        item1.submission_time = None
        item1.text = 'text bar'
        item1.kids = [2]
        item1.url = 'bar.com'
        item1.score = 20
        item1.title = 'title bar'
        item1.descendants = 1
        items.append(item1)
        item2 = MockItem()
        item2.item_id = 2
        item2.by = 'baz'
        item2.submission_time = None
        item2.text = 'text baz'
        item2.kids = []
        item2.url = 'baz.com'
        item2.score = 30
        item2.title = 'title baz'
        item2.descendants = 0
        items.append(item2)
        return items

    def _generate_mock_users(self):
        users = []
        user0 = MockUser()
        user0.user_id = 'foo'
        user0.created = None
        user0.karma = 10
        user0.submitted = [0, 2]
        users.append(user0)
        user1 = MockUser()
        user1.user_id = 'bar'
        user1.created = None
        user1.karma = 20
        user1.submitted = [1]
        users.append(user1)
        return users

    def item_ids(self, limit):
        return [item.item_id for item in self.items[:limit]]

    def all_item_ids(self):
        return [item.item_id for item in self.items]

    def get_item(self, item_id):
        item_id = int(item_id)
        try:
            if item_id < len(self.items):
                return self.items[item_id]
            else:
                raise InvalidItemID
        except IndexError:
            raise InvalidItemID

    def get_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        raise InvalidUserID

    def top_stories(self, limit=None):
        return self.item_ids(limit)

    def new_stories(self, limit=None):
        return self.item_ids(limit)

    def ask_stories(self, limit=None):
        return self.item_ids(limit)

    def best_stories(self, limit=None):
        return self.item_ids(limit)

    def show_stories(self, limit=None):
        return self.item_ids(limit)

    def job_stories(self, limit=None):
        return self.item_ids(limit)

    def next_x_stories(self, start=None, end=None, post_type=None):
        return self.all_item_ids()[start:end]
