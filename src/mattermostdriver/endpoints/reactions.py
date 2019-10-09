from .base import Base
from .posts import Posts
from .users import Users


class Reactions(Base):
    endpoint = '/reactions'

    def create_reaction(self, user, post, emoji_name, create_at):
        """Create a reaction"""
        return self.client.post(
            self.endpoint,
            options={"user_id": user.id,
                     "post_id": post.id,
                     "emoji_name": emoji_name,
                     "create_at": create_at}
		)
    
    def create(self, reaction):
        self.create_reaction(reaction.user_id, reaction.post_id, reaction.emoji_name, reaction.create_at)

	def get_reactions_of_post(self, post):
        """Get a list of reactions made by all users to a given post"""
		reactions_list = self.client.get(
			Posts.endpoint + '/' + post.id + '/' + self.endpoint,
		)
        return [Reaction(**attrs) for attrs in reactions_list]

    def delete_reaction(self, user, post, emoji_name):
        """Deletes a reaction made by a user from the given post"""
		return self.client.delete(
			Users.endpoint + '/' + user.id + '/posts/' + post.id +
			'/reactions/' + emoji_name
		)
    
    def delete(self, reaction):
        self.delete_reaction(reaction.user_id, reaction.post_id, reaction.emoji_name)


class Reaction:
    def __init__(self, user, post, emoji_name, create_at):
        self.user_id = user.id
        self.post_id = post.id
        self.emoji_name = emoji_name
        self.create_at = create_at
