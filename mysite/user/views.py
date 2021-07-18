from django.http import HttpResponse, HttpResponseRedirect,JsonResponse

from django.shortcuts import get_object_or_404, render, redirect, resolve_url
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.http import Http404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, FormView
from django.views.generic.edit import DeleteView
from .forms import PostForm, ProfileForm, CommentForm, CommentReplyForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from user.models import Post, Category, Comment, CommentReply
from postsite.models import User
from django.template.loader import render_to_string



class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.views += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['commentreply_list'] = CommentReply.objects.filter(comment_id=self.kwargs['pk']).order_by('no')

        context['comment_list'] = Comment.objects.filter(post_id=self.kwargs['pk']).order_by('no')

        return context

class SearchView(LoginRequiredMixin,TemplateView):
    template_name = 'search_view.html'

class SearchDetailView(ListView):
    model = Post
    template_name = 'search_detail.html'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (
            Q(title__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__icontains=query)
        )
        if query is not None:
            qs = super().get_queryset().filter(lookups).distinct()
            order_by_name = self.request.GET.get('order_by_name', 0)
            if order_by_name == '1':
                qs = qs.order_by('-views')
            elif order_by_name == '2':
                qs = qs.order_by('-like_count')
            elif order_by_name == '3':
                qs = qs.order_by('-created_at')
            return qs

        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('user:mypage')

    def form_valid(self, form):
        form.instance.post_user_id = self.request.user.id
        return super(CreatePostView, self).form_valid(form)

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy('user:post_detail', kwargs={'pk': self.object.id})

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('user:mypage')


class UserDetail(LoginRequiredMixin, ListView):
    template_name = 'my_page.html'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(post_user_id=self.request.user)

class IndividualPageView(LoginRequiredMixin, ListView):
    template_name = 'individualpage.html'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(post_user_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_pk = self.kwargs['pk']
        context['user'] = get_object_or_404(User, pk=user_pk)

        return context

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user_profile_update.html'
    form_class = ProfileForm
    success_url = reverse_lazy('user:mypage')

    def get_object(self):
        return self.request.user

@ login_required
def likes(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()

        return JsonResponse({'result': result, })

class CommentFormView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_post.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        post_pk = self.kwargs['pk']
        comment.post = get_object_or_404(Post, pk=post_pk)
        comment.no = Comment.objects.filter(post_id=self.kwargs['pk']).count() + 1
        comment.comment_user_id = self.request.user.id
        comment.save()
        return redirect('user:post_detail', pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['pk']
        context['post'] = get_object_or_404(Post, pk=post_pk)

        return context

class CommentReplyFormView(LoginRequiredMixin, CreateView):
    model = CommentReply
    form_class = CommentReplyForm
    template_name = 'comment_reply.html'

    def form_valid(self, form):
        comment_reply = form.save(commit=False)

        comment_pk = self.kwargs['pk']
        comment_reply.comment = get_object_or_404(Comment, pk=comment_pk)
        comment_reply.no = CommentReply.objects.filter(comment_id=self.kwargs['pk']).count() + 1
        comment_reply.reply_user_id = self.request.user.id
        comment_reply.save()
        return redirect('user:post_detail', pk=comment_reply.comment.post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['pk']
        context['comment'] = get_object_or_404(Comment, pk=comment_pk)

        return context

# エラーハンドリング

def page_not_found(request, exception):
    return render(request, '404.html', status=404)