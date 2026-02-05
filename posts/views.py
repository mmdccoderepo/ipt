from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer


def get_users(request) -> JsonResponse:
    if request.method != "GET":
        return JsonResponse({"detail": "Method not allowed"}, status=405)
    try:
        users = list(User.objects.values("id", "username", "email", "created_at"))
        return JsonResponse(users, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def create_user(request) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)
    try:
        payload = json.loads(request.body or "{}")
        username = payload["username"]
        email = payload["email"]

        user = User.objects.create(username=username, email=email)
        return JsonResponse(
            {"id": user.id, "message": "User created successfully"}, status=201
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def get_posts(request) -> JsonResponse:
    if request.method != "GET":
        return JsonResponse({"detail": "Method not allowed"}, status=405)
    try:
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
        return JsonResponse(posts, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def create_post(request) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)
    try:
        payload = json.loads(request.body or "{}")
        author_id = payload["author_id"]
        title = payload["title"]
        content = payload["content"]
        author = User.objects.get(pk=author_id)
        post = Post.objects.create(title=title, content=content, author=author)
        return JsonResponse(
            {"id": post.id, "message": "Post created successfully"}, status=201
        )
    except User.DoesNotExist:
        return JsonResponse({"detail": "Author not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
