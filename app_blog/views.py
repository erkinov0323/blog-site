from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.authtoken.models import Token


from .models import Post, Comment, Like
from .serializer import PostSerializer, SigninSerializer, SignupSerializer, ProfilSerializer, CommentSerializer, LikeSerializer



class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        

        return Response({
            "message":"SignUp",
            "data":serializer.data
        })
    

class SigninView(APIView):
    def post(self, request):
        serializer = SigninSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
      
        token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])

        return Response({
            "message":"Tasdiqlandi",
            "token":str(token.key)
        })


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ProfilSerializer(user)

        return Response({
            "message":"Profile",
            "data":serializer.data
        })
    
    
class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = ProfilSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message":"Profile update",
            "data":serializer.data
        })


class PostCreateListView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        return Response({
            "message": "list",
            "data": serializer.data
        })


    def post(self, request):

        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)

            return Response({
                "message": "created",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "error"
        }, status=status.HTTP_400_BAD_REQUEST)


class PostDetailUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        post = Post.objects.filter(id=id).first()

        serializer = PostSerializer(post)

        return Response({
            "message": "Post detail",
            "data": serializer.data
        })
    

    def patch(self, request, id):
        post = Post.objects.filter(id=id).first()

        if post.author != request.user:
            raise ValidationError({"message": "Post egasi emassiz"})

        serializer = PostSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

        return Response({
                "message": "updated",
                "data": serializer.data
        })
    

    def delete(self, request, id):
        post = Post.objects.filter(id=id).first()

        if post.author != request.user:
            raise ValidationError({"message": "Post egasi emassiz"})

        post.delete()

        return Response({
            "message": "deleted"
        })


class CommentCreateListView(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)

        return Response({
            "message":"comments",
            "data":serializer.data
        }, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response({
                "message": "created",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "error"
        }, status=status.HTTP_400_BAD_REQUEST)
    

class CommentDetailUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        post = Comment.objects.filter(id=id).first()

        serializer = CommentSerializer(post)

        return Response({
            "message": "detail",
            "data": serializer.data
        })
    

    def patch(self, request, id):
        comment = Comment.objects.filter(id=id).first()

        if comment.user != request.user:
            raise ValidationError({"message": "Comment egasi emassiz"})

        serializer = CommentSerializer(comment, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

        return Response({
                "message": "updated",
                "data": serializer.data
        })
    

    def delete(self, request, id):
        comment = Comment.objects.filter(id=id).first()

        if comment.user != request.user:
            raise ValidationError({"message": "comment egasi emassiz"})

        comment.delete()

        return Response({
            "message": "deleted"
        })
    

class LikeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        post = Post.objects.filter(id=id).first()

        if not post:
            raise ValidationError({
                "message": "Post topilmadi"
            })

        like = Like.objects.filter(
            user=request.user,
            post=post
        ).first()

        if like:
            raise ValidationError({"message": "Siz bu postga allaqachon like bosgansiz"})

        like = Like.objects.create(
            user=request.user,
            post=post
        )

        serializer = LikeSerializer(like)

        return Response({
            "message": "Like bosildi",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    

class UnlikeView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        post = Post.objects.filter(id=id).first()

        if not post:
            raise ValidationError({
                "message": "Post topilmadi"
            })

        like = Like.objects.filter(
            user=request.user,
            post=post
        ).first()

        if not like:
            raise ValidationError({
                "message": "Like topilmadi"
            })

        like.delete()

        return Response({
            "message": "Like olib tashlandi"
        })