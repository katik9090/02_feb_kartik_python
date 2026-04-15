from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import BlogPostSerializer, CommentSerializer
from django.shortcuts import get_object_or_404


# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def post_list_create(request):
    if request.method == 'GET':
        posts = BlogPost.objects.all().order_by('-created_at')
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'error': 'Login required'}, status=401)
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# ✅ Retrieve, update or delete a post
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'GET':
        serializer = BlogPostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user != post.author:
            return Response({'error': 'You can edit only your post'}, status=403)
        serializer = BlogPostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if request.user != post.author:
            return Response({'error': 'You can delete only your post'}, status=403)
        post.delete()
        return Response(status=204)


# ✅ Comments
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def comments_view(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'GET':
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'error': 'Login required'}, status=401)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Return the current logged-in user's data"""
    user = request.user  # comes automatically from the JWT token
    data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }
    return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])  # anyone can register
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    # Validation
    if not username or not email or not password:
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()

    return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)