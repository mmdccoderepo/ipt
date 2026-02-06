from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly

from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer


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
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            # Bridge: Find the local User that matches the logged-in Auth User
            try:
                author_user = User.objects.get(username=request.user.username)
            except User.DoesNotExist:
                # Fallback: If no local user exists, reject or auto-create. 
                # For safety, let's reject and tell them to create a User profile first.
                return Response(
                    {"error": "No matching User profile found for this account."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(author=author_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListCreate(APIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
             # Bridge: Find the local User that matches the logged-in Auth User
            try:
                author_user = User.objects.get(username=request.user.username)
            except User.DoesNotExist:
                return Response(
                    {"error": "No matching User profile found for this account."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save(author=author_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
