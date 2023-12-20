from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegisterationForm, UserLoginForm, PostUpdateForm, CreateNewPostForm, CreateCommentForm, EditUserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PostModel, FollowUnFollowModel, LikeModel
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

class RegisterationView(View):
    form_class = UserRegisterationForm
    template_name = 'accounts/Register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('Home:Home')
        return super().dispatch(request, *args ,**kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username = cd['username'], email = cd['email'], password = cd['password'])
            messages.success(request, 'Your account has been registered successfully', 'success')
            return redirect('Home:Home')
        return render(request, self.template_name, {'form':form})

class LoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/Login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('Home:Home')
        return super().dispatch(request, *args ,**kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password = cd['password'])
            if user:
                login(request, user)
                messages.success(request, 'Welcome, ' + user.username + '!', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('Home:Home')
            else:
                messages.warning(request,'Username, Email or Password is incorrect, Otherwise user does not exists.', 'danger')
                return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})

class LogOutView(LoginRequiredMixin ,View):
    def get(self, request):
        messages.success(request, 'See you later, ' + request.user.username + '.', 'success')
        logout(request)
        return redirect('Home:Home')

class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/Profile.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, pk = user_id)
        is_following = user.Following.filter(FollowerUser= request.user).exists()
        Posts = user.posts.all()
        return render(request, self.template_name, {'user':user, 'Posts':Posts, 'is_following':is_following})

class PostDetailView(LoginRequiredMixin ,View):
    template_name = 'accounts/PostDetail.html'
    form_class = CreateCommentForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(PostModel, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        self.comments = self.post_instance.pcomment.filter(is_reply=False)
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'post':self.post_instance, 'comments':self.comments, 'form':self.form_class})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'Your comment has been submitted successfully', 'success')
            return redirect('accounts:PostDetail', self.post_instance.id, self.post_instance.slug)
        return render(request, self.template_name, {'post':self.post_instance, 'comments':self.comments, 'form':self.form_class})

class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(PostModel, pk= post_id)
        if request.user.id == post.creator.id:
            post.delete()
            messages.success(request, 'The post has been deleted successfully', 'success')
        else:
            messages.warning(request, "You can't delete this post because it's not yours", 'danger')
        return redirect('Home:Home')

class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm
    template_name = 'accounts/PostUpdate.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(PostModel, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not request.user.id == post.creator.id:
            messages.warning(request, "You can't update this form because it's not yours", 'danger')
            return redirect('Home:Home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance= post)
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = PostUpdateForm(request.POST, instance= post)
        if form.is_valid():
            updated_post = form.save(commit= False)
            updated_post.slug = slugify(form.cleaned_data['title'])
            updated_post.save()
            messages.success(request, "Your post has been updated successfully", 'success')
            return redirect('accounts:PostDetail', updated_post.id, updated_post.slug)
        return render(request, self.template_name, {'form':form})

class CreateNewPostView(LoginRequiredMixin, View):
    form_class = CreateNewPostForm
    template_name = 'accounts/CreateNewPost.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit= False)
            new_post.creator = request.user
            new_post.slug = slugify(form.cleaned_data['title'])
            new_post.save()
            messages.success(request, "Your new post has been created successfully", 'success')
            return redirect('accounts:Profile', request.user.id)
        return render(request, self.template_name, {'form':form})

class ResetPasswordView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:PasswordResetDone')
    email_template_name = 'accounts/password_reset_email.html'

class PasswrodResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/PasswordResetConfirm.html'
    success_url = reverse_lazy('accounts:PassResetCompleted')

class PasswordResetCompletedView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/PasswordResetCompleted.html'

class FollowView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['user_id'])
        fs = FollowUnFollowModel.objects.filter(FollowedUser = user, FollowerUser = request.user).exists()
        if fs:
            messages.error(request, 'You already followed this user', 'danger')
        else:
            FollowUnFollowModel.objects.create(FollowerUser = request.user, FollowedUser = user)
            messages.success(request, 'You followed this user successfully', 'success')
        return redirect('accounts:Profile', kwargs['user_id'])

class UnFollowView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['user_id'])
        fs = FollowUnFollowModel.objects.filter(FollowedUser = user, FollowerUser = request.user).exists()
        if fs:
            fs = user.Following.get(FollowerUser= request.user)
            fs.delete()
            messages.success(request, 'You unfollowed this user successfully', 'success')
        else:
            messages.error(request, 'You are not following this user', 'danger')
        return redirect('accounts:Profile', kwargs['user_id'])

class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(PostModel, id=kwargs['post_id'])
        did_liked = LikeModel.objects.filter(post=post, user=request.user)
        if did_liked.exists():
            messages.error(request, 'You already liked this post', 'danger')
        else:
            LikeModel.objects.create(user=request.user, post=post)
        return redirect('accounts:PostDetail', post.id, post.slug)

class EditProfileView(LoginRequiredMixin, View):
    form_class = EditUserProfileForm
    template_name = 'accounts/EditProfile.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user.GeneralInfo, initial={
            'email': request.user.email, 'username': request.user.username})
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user.GeneralInfo)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.username = form.cleaned_data['username']
            request.user.save()
            messages.success(request, 'Your profile has been updated successfully', 'success')
            return redirect('accounts:Profile', request.user.id)
        return render(request, self.template_name, {'form':form})