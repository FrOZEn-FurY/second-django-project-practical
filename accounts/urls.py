from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.RegisterationView.as_view(), name ='Registeration'),
    path('login/', views.LoginView.as_view(), name ='Login'),
    path('logout/', views.LogOutView.as_view(), name ='Logout'),
    path('profile/<int:user_id>', views.ProfileView.as_view(), name='Profile'),
    path('profile/post/<int:post_id>/<str:post_slug>', views.PostDetailView.as_view(), name='PostDetail'),
    path('delete/<int:post_id>/', views.PostDeleteView.as_view(), name='PostDelete'),
    path('update/<int:post_id>/', views.PostUpdateView.as_view(), name='PostUpdate'),
    path('createpost/', views.CreateNewPostView.as_view(), name='CreateNewPost'),
    path('resetpass/', views.ResetPasswordView.as_view(), name='ResetPassword'),
    path('resetpass/done/', views.PasswrodResetDoneView.as_view(), name='PasswordResetDone'),
    path('resetpass/confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='PassResetConfirm'),
    path('resetpass/complete/', views.PasswordResetCompletedView.as_view(), name='PassResetCompleted'),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='Follow'),
    path('unfollow/<int:user_id>/', views.UnFollowView.as_view(), name='UnFollow'),
    path('like/<int:post_id>/', views.PostLikeView.as_view(), name='Like'),
    path('editprofile/', views.EditProfileView.as_view(), name='EditProfile'),
]