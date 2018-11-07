from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post


# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog_app/home.html', context)


class PostListView(ListView):
    # By convention it looks for template  with this name: <app_name>/<model_name>_list
    model = Post
    template_name = 'blog_app/home.html'
    context_object_name = 'posts'
    paginate_by = 5


class UserPostListView(ListView):
    # By convention it looks for template  with this name: <app_name>/<model_name>_list
    model = Post
    template_name = 'blog_app/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        # 'self.kwargs.get' - get parameters from the url
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user)


class PostDetailView(DetailView):
    # By convention it looks for template  with this name: <app_name>/<model_name>_detail
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    # By convention it looks for template  with this name: <app_name>/<model_name>_form
    model = Post
    fields = ['title', 'content']
    # success_url - After success port redirect user to specified url

    def form_valid(self, form):
        """ Send user data to Post form """
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # By convention it looks for template with this name: <app_name>/<model_name>_form
    model = Post
    fields = ['title', 'content']
    # success_url - After success port redirect user to specified url

    def form_valid(self, form):
        """ Send user data to Post form """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """
        It's method from 'UserPassesTestMixin'. Should be overwritten
        Prevent updating posts from other users
        """
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # By convention it looks for template with this name: <app_name>/<model_name>_confirm_delete
    model = Post
    success_url = '/'  # After deleting an object redirect user to given url path (it's our home page)

    def test_func(self):
        """
        It's method from 'UserPassesTestMixin'. Should be overwritten
        Prevent updating posts from other users
        """
        post = self.get_object()
        return self.request.user == post.author


def about(request):
    return render(request, 'blog_app/about.html', {'title': 'about'})
