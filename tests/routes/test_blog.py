"""
Blog route tests.
"""

import pytest
from httpx import AsyncClient

from tests.util import auth_headers
from tests.data import add_empty_user, add_blog_post


@pytest.mark.asyncio
async def test_blog_get(client: AsyncClient) -> None:
    """Test getting all blog posts"""
    resp = await client.get("/blog")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 0


@pytest.mark.asyncio
async def test_blog_post(client: AsyncClient) -> None:
    """Test creating a blog post"""
    blog_post = {"title": "Test", "content": "Test content"}
    resp = await client.post("/blog", json=blog_post)
    assert resp.status_code == 401
    data = resp.json()
    assert data["detail"] == "Missing Authorization Header"


@pytest.mark.asyncio
async def test_blog_post_auth(client: AsyncClient) -> None:
    """Test creating a blog post"""
    blog_post = {"title": "Test", "content": "Test content"}
    await add_empty_user()
    email = "empty@test.io"
    auth = await auth_headers(client, email)
    resp = await client.post("/blog", json=blog_post, headers=auth)
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == blog_post["title"]
    assert data["content"] == blog_post["content"]
    assert data["author"]["email"] == email


@pytest.mark.asyncio
async def test_blog_get_one_none(client: AsyncClient) -> None:
    """Test getting a blog post"""
    resp = await client.get("/blog/Test")
    assert resp.status_code == 404
    data = resp.json()
    assert data["detail"] == "Blog post not found"


@pytest.mark.asyncio
async def test_blog_get_one(client: AsyncClient) -> None:
    """Test getting a blog post"""
    await add_blog_post()
    resp = await client.get("/blog/Test")
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Test"
    assert data["content"] == "Test content"
    assert data["author"]["email"] == "empty@test.io"


@pytest.mark.asyncio
async def test_blog_put_none(client: AsyncClient) -> None:
    """Test updating a blog post"""
    blog_post = {"title": "Test", "content": "Test content"}
    resp = await client.put("/blog/Test", json=blog_post)
    assert resp.status_code == 401
    data = resp.json()
    assert data["detail"] == "Missing Authorization Header"
