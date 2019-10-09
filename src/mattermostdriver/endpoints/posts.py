from .base import Base
from .teams import Teams
from .users import Users
from .channels import Channels


class Posts(Base):
	endpoint = '/posts'

	def create_post(self, channel_id, message, root_id=None, file_ids=None, props=None):
		"""Create a new post in a channel. To create the post as a comment on another post, provide `root_id`."""
		return self.client.post(
			self.endpoint,
			options={"channel_id": channel_id,
					 "message": message,
					 "root_id": root_id,
					 "file_ids": file_ids,
					 "props": props}
		)

	def create_ephemeral_post(self, user_id, channel_id, message):
		"""Create a new ephemeral post in a channel. (currently only given to system admin)"""
		return self.client.post(
			self.endpoint + '/ephemeral',
			options={"user_id": user_id,
					 "post": {"channel_id": channel_id, "message": message}}
		)

	def get_post(self, post_id):
		return self.client.get(
			self.endpoint + '/' + post_id,
		)

	def delete_post(self, post_id):
		return self.client.delete(
			self.endpoint + '/' + post_id,
		)

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

	def get_thread(self, post_id):
		return self.client.get(
			self.endpoint + '/' + post_id + '/thread',
		)

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
