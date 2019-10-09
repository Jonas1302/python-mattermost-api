from .base import Base
from .posts import Posts
from .users import Users


class Reactions(Base):
	endpoint = '/reactions'

	def create_reaction(self, user_id, post_id, emoji_name, create_at):
        """Create a reaction"""
		return self.client.post(
			self.endpoint,
			options={"user_id": user_id,
                     "post_id": post_id,
                     "emoji_name": emoji_name,
                     "create_at": create_at}
		)

	def get_reactions_of_post(self, post_id):
        """Get a list of reactions made by all users to a given post"""
		return self.client.get(
			Posts.endpoint + '/' + post_id + '/' + self.endpoint,
		)

	def delete_reaction(self, user_id, post_id, emoji_name):
        """Deletes a reaction made by a user from the given post"""
		return self.client.delete(
			Users.endpoint + '/' + user_id + '/posts/' + post_id +
			'/reactions/' + emoji_name
		)
