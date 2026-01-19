import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Post, User


def list_users(request) -> JsonResponse:
    if request.method != "GET":
        return JsonResponse({"detail": "Method not allowed"}, status=405)
    users = list(
        User.objects.values("id", "username", "email", "bio", "profile_picture")
    )
    return JsonResponse({"users": users}, status=200)


@csrf_exempt
def create_user(request) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)
    try:
        payload = json.loads(request.body or "{}")
        username = payload["username"]
        email = payload["email"]
        bio = payload.get("bio", "")
    except (KeyError, json.JSONDecodeError):
        return JsonResponse({"detail": "Invalid payload"}, status=400)

    user = User.objects.create(username=username, email=email, bio=bio)
    return JsonResponse(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "bio": user.bio,
        },
        status=201,
    )


def list_posts(request) -> JsonResponse:
    if request.method != "GET":
        return JsonResponse({"detail": "Method not allowed"}, status=405)
    posts = list(
        Post.objects.select_related("author")
        .all()
        .values(
            "id",
            "title",
            "content",
            "created_at",
            "updated_at",
            "author_id",
            "author__username",
            "author__email",
        )
    )
    return JsonResponse({"posts": posts}, status=200)


@csrf_exempt
def create_post(request) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)
    try:
        payload = json.loads(request.body or "{}")
        author_id = payload["author_id"]
        title = payload["title"]
        content = payload["content"]
    except (KeyError, json.JSONDecodeError):
        return JsonResponse({"detail": "Invalid payload"}, status=400)

    try:
        author = User.objects.get(pk=author_id)
    except User.DoesNotExist:
        return JsonResponse({"detail": "Author not found"}, status=404)

    post = Post.objects.create(author=author, title=title, content=content)
    return JsonResponse(
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_id": author.id,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
        },
        status=201,
    )
