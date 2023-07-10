"""
# Blog router
# """

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response

from myserver.models.blog import BlogPost, BlogPostDB, BlogPostOut
from myserver.models.user import User
from myserver.util.current_user import current_user

router = APIRouter(prefix="/blog", tags=["Blog"])


@router.get("", response_model=List[BlogPostOut])
async def get_blog_posts():
    """Get all blog posts"""
    return await BlogPostDB.find({}).to_list()


@router.get("/{title}", response_model=BlogPostOut)
async def get_blog_post(title: str):
    """Get a blog post by title"""
    post = await BlogPostDB.by_title(title)
    if post is None:
        raise HTTPException(404, "Blog post not found")
    return post


@router.post("", response_model=BlogPostOut)
async def create_blog_post(blog_post: BlogPost,
                           user: User = Depends(current_user)):
    """Create a new blog post"""
    post = BlogPostDB(**blog_post.dict(), author=user)
    await post.create()
    return post


@router.put("/{title}", response_model=BlogPostOut)
async def update_blog_post(title: str,
                           blog_post: BlogPost,
                           user: User = Depends(current_user)):
    """Update an existing blog post"""
    post = await BlogPostDB.by_title(title)
    if post is None:
        raise HTTPException(404, "Blog post not found")
    if post.author != user:
        raise HTTPException(403, "You are not the author of this post")
    await post.update(**blog_post.dict())
    return post


@router.delete("/{title}")
async def delete_blog_post(title: str, user: User = Depends(current_user)):
    """Delete a blog post"""
    post = await BlogPostDB.by_title(title)
    if post is None:
        raise HTTPException(404, "Blog post not found")
    if post.author != user:
        raise HTTPException(403, "You are not the author of this post")
    await post.delete()
    return Response(status_code=204)
