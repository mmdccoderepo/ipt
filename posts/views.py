from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from posts.factories.post_factory import PostFactory
from posts.singletons.logger_singleton import (
    LoggerSingleton,
)
from .models import Post, Comment
from .permissions import IsPostAuthor
from .serializers import UserSerializer, PostSerializer, CommentSerializer


logger = LoggerSingleton().get_logger()


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(
                {"detail": "Username and password required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(username=username, password=password)
        if not user:
            logger.warning(f"Failed login attempt for username: {username}")
            return Response(
                {"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST
            )
        token, _ = Token.objects.get_or_create(user=user)
        request.session["token"] = token.key  # Store token in session cookie
        logger.info(f"User {username} logged in and token stored in session.")
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class UserListCreate(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsPostAuthor]

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        self.check_object_permissions(request, post)
        return Response({"content": post.content})


class CreatePostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        try:
            post = PostFactory.create_post(
                post_type=data["post_type"],
                author=user,
                title=data["title"],
                content=data.get("content", ""),
                metadata=data.get("metadata", {}),
            )
            return Response(
                {"message": "Post created successfully!", "post_id": post.id},
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CommentListCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
