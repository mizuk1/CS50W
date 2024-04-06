from django.contrib.auth.models import AbstractUser
from django.db import models


# represents each user of the application
class User(AbstractUser):
    # Show the email of the user
    def __str__(self) -> str:
        return self.email

# represents each post
class Post(models.Model):
    # the author of the post
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # serialize the values into a dictionary
    def serialize(self):
        return {
            "user": self.user.username,
            "text": self.text,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

    def __str__(self) -> str:
        return f"Post {self.id} by {self.user} on {self.timestamp}"

# represents each like
class Like(models.Model):
    # user who liked the post
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    
    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user} likes {self.post.id}"

# represents follows
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower} follows {self.followed}"