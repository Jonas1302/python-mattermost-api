import logging
from .base import Base
from .teams import Teams
from .users import Users

log = logging.getLogger('mattermostdriver.api.channels')
log.setLevel(logging.INFO)


class Channel:
    def __init__(self, id, name, display_name, **kwargs):
        """`name`: unique name; `display_name`: non-unique channel name"""
        self.id = id
        self.name = name
        self.display_name = display_name
        self.__dict__.update(kwargs)


class Channels(Base):
    endpoint = '/channels'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users = Users(self.client)

    def create_channel(self, team_id, name, deisplay_name, type_, purpose=None, header=None):
        """'O' for a public channel, 'P' for a private channel"""
        return Channel(**self.client.post(
            self.endpoint,
            {"team_id": team_id,
             "name": name,
			 "display_name": deisplay_name,
             "purpose": purpose,
             "header": header,
             "type": type_}
        ))
    
    def create_public_channel(self, team_id, name, deisplay_name, purpose=None, header=None):
        return self.create_channel(team_id, name, deisplay_name, "O", purpose=None, header=None)
    
    def create_private_channel(self, team_id, name, deisplay_name, purpose=None, header=None):
        return self.create_channel(team_id, name, deisplay_name, "P", purpose=None, header=None)

    def create_direct_message_channel(self, current_user_id, other_user_id):
        return Channel(**self.client.post(
            self.endpoint + '/direct',
            [current_user_id, other_user_id]
        ))

    def create_group_message_channel(self, *user_ids):
        return Channel(**self.client.post(
            self.endpoint + '/group',
            user_ids
        ))

    def get_list_of_channels_by_ids(self, team_id, *channel_ids):
        response = self.client.post(
            Teams.endpoint + '/' + team_id + '/channels/ids',
            channel_ids
        )
        return [Channel(**attrs) for attrs in response]

    def get_channel(self, channel_id):
        return Channel(**self.client.get(self.endpoint + '/' + channel_id))

    def update_channel(self, channel_id, options):
        return self.client.put(
            self.endpoint + '/' + channel_id,
            options=options
        )

    def delete_channel(self, channel_id):
        return self.client.delete(
            self.endpoint + '/' + channel_id
        )

    def patch_channel(self, channel_id, options):
        return self.client.put(
            self.endpoint + '/' + channel_id + '/patch',
            options=options
        )

    def restore_channel(self, channel_id):
        return self.client.post(
            self.endpoint + '/' + channel_id + '/restore',
        )

    def get_channel_statistics(self, channel_id):
        return self.client.get(
            self.endpoint + '/' + channel_id + '/stats',
        )

    def get_channel_pinned_posts(self, channel_id):
        return self.client.get(
            self.endpoint + '/' + channel_id + '/pinned'
        )

    def get_channel_by_name(self, team, channel_name, include_deleted=False):
        """Gets channel from the provided team id and channel name strings."""
        return Channel(**self.client.get(
            Teams.endpoint + '/' + team.id + '/channels/name/' + channel_name,
            params={"include_deleted": include_deleted}
        ))

    def get_channel_members(self, channel, page=0, per_page=1<<10):
        """Get a page of members for a channel."""
        response = self.client.get(
            self.endpoint + '/' + channel.id + '/members',
            params={"page": page,
                    "per_page": per_page}
        )
        return self.users.get_users_by_ids(*[attrs["user_id"] for attrs in response])
        

    def add_user(self, channel_id, user_id, post_root_id=None):
        """Add a user to a channel by creating a channel member object."""
        return self.client.post(
            self.endpoint + '/' + channel_id + '/members',
            {"user_id": user_id,
             "post_root_id": post_root_id}
        )

    def get_channel_members_by_ids(self, channel_id, *user_ids):
        """Get a list of channel members based on the provided user ids."""
        return self.client.post(
            self.endpoint + '/' + channel_id + '/members/ids',
            options=user_ids
        )

    def get_channel_member(self, channel_id, user_id):
        """Get a channel member."""
        return self.client.get(
            self.endpoint + '/' + channel_id + '/members/' + user_id
        )

    def remove_channel_member(self, channel_id, user_id):
        """Delete a channel member, effectively removing them from a channel."""
        return self.client.delete(
            self.endpoint + '/' + channel_id + '/members/' + user_id
        )

    def update_channel_roles(self, channel_id, user_id, roles):
        """Update a user's roles for a channel."""
        return self.client.put(
            self.endpoint + '/' + channel_id + '/members/' + user_id + '/roles',
            options={"roles": roles}
        )

    def update_channel_notifications(self, channel_id, user_id, options=None):
        return self.client.put(
            self.endpoint + '/' + channel_id + '/members/' + user_id + '/notify_props',
            options=options
        )

    def view_channel(self, user_id, options):
        return self.client.post(
            self.endpoint + '/members/' + user_id + '/view',
            options=options
        )

    def get_channel_members_for_user(self, user_id, team_id):
        """Get all channel members on a team for a user."""
        return self.client.get(
            Users.endpoint + '/' + user_id + '/teams/' + team_id + '/channels/members'
        )

    def get_channels_for_user(self, user_id, team_id):
        """Get all the channels on a team for a user."""
        return self.client.get(
            Users.endpoint + '/' + user_id + '/teams/' + team_id + '/channels'
        )

    def get_unread_messages(self, user_id, channel_id):
        return self.client.get(
            Users.endpoint + '/' + user_id + '/channels/' + channel_id + '/unread'
        )

    def get_public_channels(self, team, page=0, per_page=1<<10):
        response = self.client.get(
            '/teams/' + team.id + '/channels',
            params={"page": page,
                    "per_page": per_page}
        )
        return [Channel(**attrs) for attrs in response]

    def get_deleted_channels(self, team, page=0, per_page=1<<10):
        response = self.client.get(
            '/teams/' + team.id + '/channels/deleted',
            params={"page": page,
                    "per_page": per_page}
        )
        return [Channel(**attrs) for attrs in response]

    def search_channels(self, team_id, options=None):
        return self.client.post(
            '/teams/' + team_id + '/channels/search',
            options=options
        )

    def autocomplete_channels(self, team_id, params=None):
        return self.client.get(
            '/teams/' + team_id + '/channels/autocomplete',
            params=params
        )

    def update_scheme_derived_roles_of_channel_member(self, channel_id, user_id, options=None):
        return self.client.put(
            self.endpoint + '/' + channel_id + '/members/' + user_id + '/schemeRoles',
            options=options
        )

    def set_channel_scheme(self, channel_id):
        return self.client.put(
            self.endpoint + '/' + channel_id + '/scheme'
        )

    def convert_channel(self, channel_id):
        return self.client.post(
            self.endpoint + '/' + channel_id + '/convert'
        )