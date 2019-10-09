from .base import Base
from .teams import Teams
from .users import Users
from .channels import Channels


class Post:
    def __init__(self, endpoint, id, **kwargs):
        self.endpoint = endpoint
        self.__dict__.update(kwargs)
        
        if "user" in kwargs:
            self.user_id = kwargs["user"].id
        if "channel" in kwargs:
            self.channel_id = kwargs["channel"].id
        if "root" in kwargs:
            self.root_id = kwargs["root"].id
        if "parent" in kwargs:
            self.parent_id = kwargs["parent"].id
        if "original" in kwargs:
            self.original_id = kwargs["original"].id
    
    @property
    def user(self):
        return self.endpoint.users.get_user(self.user_id)
    
    @property
    def channel(self):
        return self.endpoint.channels.get_channel(self.channel_id)
    
    @property
    def root(self):
        return self.endpoint.get_post(self.root_id)
    
    @property
    def parent(self):
        return self.endpoint.get_post(self.parent_id)
        
    @property
    def original(self):
        return self.endpoint.get_post(self.original_id)


class Thread:
    def __init__(self, endpoint, order, posts, next_post_id, prev_post_id):
        self.endpoint = endpoint
        self._post_ids = order
        self.next_post_id = next_post_id
        self.prev_post_id = prev_post_id
    
    @property
    def posts(self):
        return [self.endpoint.get_post(pid) for pid in self._post_ids]
    
    @property
    def next_post(self):
        return self.endpoint.get_post(self.next_post_id)
    
    @property
    def previous_post(self):
        return self.endpoint.get_post(self.prev_post_id)

class Posts(Base):
    endpoint = '/posts'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users = Users(self.client)
        self.channels = Channels(self.client)

    def create_post(self, channel, message, root=None, file_ids=None, props=None):
        """Create a new post in a channel. To create the post as a comment on another post, provide `root`."""
        return Post(self, **self.client.post(
            self.endpoint,
            options={"channel_id": channel.id,
                     "message": message,
                     "root_id": root.id,
                     "file_ids": file_ids,
                     "props": props}
        ))

    def create_ephemeral_post(self, user, channel, message):
        """Create a new ephemeral post in a channel. (currently only given to system admin)"""
        return Post(self, **self.client.post(
            self.endpoint + '/ephemeral',
            options={"user_id": user.id,
                     "post": {"channel_id": channel.id, "message": message}}
        ))

    def get_post(self, post_id):
        return Post(self, **self.client.get(self.endpoint + '/' + post_id))

    def delete_post(self, post):
        return self.client.delete(self.endpoint + '/' + post.id)

    def update_post(self, post_id, is_pinned=None, message=None, has_reactions=True, props=None):
        """`patch_post` SEEMS to be preferred as it leaves the `is_pinned` status when `None`"""
        return self.client.put(
            self.endpoint + '/' + post_id,
            options={"id": post_id,
                     "is_pinned": is_pinned,
                     "message": message,
                     "has_reactions": has_reactions,
                     "props": props}
        )

    def patch_post(self, post_id, is_pinned=None, message=None, has_reactions=True, props=None):
        return self.client.put(
            self.endpoint + '/' + post_id + '/patch',
            options={"id": post_id,
                     "is_pinned": is_pinned,
                     "message": message,
                     "has_reactions": has_reactions,
                     "props": props}
        )

    def get_thread(self, post):
        return Thread(self, **self.client.get(self.endpoint + '/' + post.id + '/thread'))

    def get_list_of_flagged_posts(self, user_id, params=None):
        return self.client.get(
            Users.endpoint + '/' + user_id + '/posts/flagged',
            params=params
        )

    def get_file_info_for_post(self, post_id):
        return self.client.get(
            self.endpoint + '/' + post_id + '/files/info',
        )

    def get_posts_for_channel(self, channel_id, params=None):
        return self.client.get(
            Channels.endpoint + '/' + channel_id + '/posts',
            params=params
        )

    def search_for_team_posts(self, team_id, options):
        return self.client.post(
            Teams.endpoint + '/' + team_id + '/posts/search',
            options=options
        )

    def pin_post_to_channel(self, post_id):
        return self.client.post(
            self.endpoint + '/' + post_id + '/pin'
        )

    def unpin_post_to_channel(self, post_id):
        return self.client.post(
            self.endpoint + '/' + post_id + '/unpin'
        )

    def perform_post_action(self, post_id, action_id):
        return self.client.post(
            self.endpoint + '/' + post_id + '/actions/' + action_id
        )
