"""
Blog model
"""

from datetime import datetime
from typing import Optional

from beanie import Document, Indexed
from pydantic import BaseModel

from myserver.models.user import UserOut


class BlogPost(BaseModel):
    """Blog post"""

    title: str
    content: str
    created: Optional[datetime] = None


class BlogPostUpdate(BaseModel):
    """Updatable blog post fields"""

    title: Optional[str] = None
    content: Optional[str] = None


class BlogPostOut(BlogPostUpdate):
    """Blog post fields returned to the client"""
    author: UserOut


class BlogPostDB(Document, BlogPostOut):
    """Blog post DB representation"""


    def __repr__(self) -> str:
        return f"<BlogPost {self.title}>"
    
    def __str__(self) -> str:
        return self.title
    
    def __hash__(self) -> int:
        return hash(self.title)
    
    def __eq__(self, other: object) -> bool:
        
        if isinstance(other, BlogPost):
            return self.title == other.title
        return False
    
    @property
    def created(self) -> datetime:
        
        return self.id.generation_time

    @classmethod
    async def by_title(cls, title: str) -> "BlogPost":
        """Get a blog post by title"""
        return await cls.find_one(cls.title == title)
    