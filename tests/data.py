"""
Test data handlers
"""

from datetime import datetime, timezone

from myserver.models.user import User
from myserver.util.password import hash_password
from myserver.models.blog import BlogPostDB


async def add_empty_user() -> User:
    """Adds test users to user collection"""
    empty_user = User(
        email="empty@test.io",
        password=hash_password("empty@test.io"),
        email_confirmed_at=datetime.now(tz=timezone.utc),
    )
    await empty_user.create()
    return empty_user


async def add_blog_post() -> None:
    """Adds test blog post to blog collection"""
    blog = BlogPostDB(
        title="Test",
        content="Test content",
        author=await add_empty_user(),
    )
    await blog.create()
