from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.SignupView.as_view()),
    path('signin', views.SigninView.as_view()),
    path("profile", views.ProfileView.as_view()),
    path("profile-update", views.ProfileUpdateView.as_view()),

    path('post/create-list', views.PostCreateListView.as_view()),
    path('post/detail-update-delete/<int:id>', views.PostDetailUpdateDeleteView.as_view()),

    path('comment/create-list', views.CommentCreateListView.as_view()),
    path('comment/detail-update-delete/<int:id>', views.CommentDetailUpdateDeleteView.as_view()),

    path('like/<int:id>', views.LikeCreateView.as_view()),
    path('unlike/<int:id>', views.UnlikeView.as_view()),
]
