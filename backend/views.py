from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db import IntegrityError

from backend.models import Post
from backend.serializers import RegistrationSerializer, CreatePostSerializer


class RegisterView(APIView):

    def post(self, request):
        try:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                account = serializer.save()
                return JsonResponse({'Status': True, 'Email': account.email})
            else:
                return JsonResponse({'Status': False, 'Errors': serializer.errors})
        except IntegrityError as error:
            return JsonResponse({'Status': False, 'Errors': f'{str(error)}'})


class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        request.data['user'] = user_id
        serializer = CreatePostSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse({'Status': False, 'Errors': serializer.errors})
        serializer.save()
        return JsonResponse({'Status': True})


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        user = request.user
        post = Post.objects.filter(id=post_id).prefetch_related('likes').first()
        if not post:
            return JsonResponse({'Status': False, 'Error': 'Post not found'})
        if user in post.likes.all():
            post.likes.remove(user)
            post.save()
            like_status = False
        else:
            post.likes.add(user)
            post.save()
            like_status = True
        return JsonResponse({'Status': True, 'Like_status': like_status})
