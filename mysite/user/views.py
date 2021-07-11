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
from .forms import PostForm, ProfileForm, CommentForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from user.models import Post, Category, Comment
from postsite.models import User
from django.template.loader import render_to_string



class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset=queryset)
    #     if not obj.is_public and not self.request.user.is_authenticated:
    #         raise Http404
    #     return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.views += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['comment_list'] = Comment.objects.filter(post_id=self.kwargs['pk']).order_by('no')

        return context



    # def get_object(self):
    #     return self.request.user

class SearchView(TemplateView):
    template_name = 'search_view.html'


@method_decorator(login_required, name='dispatch')
class IndexView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'index.html'

    paginate_by = 5


class CategoryListView(ListView):
    queryset = Category.objects.annotate(
        num_posts=Count('post', filter=Q(post__is_public=True)))


class SearchDetailView(ListView):
    model = Post
    template_name = 'search_detail.html'
    paginate_by = 1

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



# class SearchPostView(ListView):
#     model = Post
#     template_name = 'search_post.html'
#     paginate_by = 3

#     def get_queryset(self):
#         query = self.request.GET.get('q', None)
#         lookups = (
#             Q(title__icontains=query) |
#             Q(category__name__icontains=query) |
#             Q(tags__icontains=query)
#         )
#         if query is not None:
#             qs = super().get_queryset().filter(lookups).distinct()
#             return qs
#         qs = super().get_queryset()
#         # return qs
#         return JsonResponse(qs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         query = self.request.GET.get('q')
#         context['query'] = query
#         return context

# class SearchPostView(ListView):
#     model = Post
#     template_name = 'search_post.html'
#     paginate_by = 3

#     def get_queryset(self):
#         query = self.request.GET.get('q', None)
#         lookups = (
#             Q(title__icontains=query) |
#             Q(category__name__icontains=query) |
#             Q(tags__icontains=query)
#         )
#         if query is not None:
#             qs = super().get_queryset().filter(lookups).distinct()
#             sort_by = self.request.GET.get('sort_by', None)
#             if sort_by == "views":
#                 qs == qs.order_by("views")
#             elif sort_by == "like_count":
#                 qs = qs.order_by("like_count")
#             data = serialize("json", qs, fields=('views', 'like_count'))

#             return JsonResponse(data, safe=False)
#         qs = super().get_queryset()
#         return qs

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     query = self.request.GET.get('q')
        # sort_by = self.request.GET.get('sort_by', None)
        # if sort_by == "views":
        #     query = query.order_by("views")
        # elif sort_by == "like_count":
        #     query = query.order_by("like_count")


        # context['query'] = query
        # return JsonResponse(context)

@method_decorator(login_required, name='dispatch')
class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'comment_form.html'
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

@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('user:mypage')


class UserDetail(LoginRequiredMixin, ListView):
    """ユーザーの詳細ページ"""
    # model = Post
    template_name = 'my_page.html'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(post_user_id=self.request.user)

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

    
    




# class CommentView(LoginRequiredMixin, CreateView):
#     model = Comment
#     template_name = 'comment_form2.html'
#     form_class = CommentForm
#     success_url = reverse_lazy('user:post_detail')

#     def get_context_data(self):
#         context = super().get_context_data()
#         context['post'] = Post.objects.get(id=self.kwargs['pk'])
#         context['comment_list'] = Comment.objects.filter(
#                 post_id=self.kwargs['pk']).order_by('no')
#         return context
    
#     def form_valid(self, form):
#         forms.save_with_post(self.kwargs.get('pk'))
#         return super(CommentView, self).form_valid(form)

# class CommentView(FormView):
#     template_name = 'post_detail.html'
#     form_class = CommentForm

#     def get_object(self, queryset=None):
#         obj = super().get_object(queryset=queryset)
#         if not obj.is_public and not self.request.user.is_authenticated:
#             raise Http404
#         return obj

#     # def get(self, request, *args, **kwargs):
#     #     self.object = self.get_object()
#     #     self.object.views += 1
#     #     self.object.save()
#     #     context = self.get_context_data(object=self.object)
#     #     return self.render_to_response(context)

#     def form_valid(self, form):
#         forms.save_with_post(self.kwargs.get('pk'))
#         return super(CommentView, self).form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy('user:post_detail', kwargs={'pk': self.kwargs['pk']})



#     def get_context_data(self):
#         context = super().get_context_data()
#         context['post'] = Post.objects.get(id=self.kwargs['pk'])
#         context['comment_list'] = Comment.objects.filter(
#                 target_id=self.kwargs['pk']).order_by('no')
#         return context


# @ login_required
# def likes(request):
    
#     post = get_object_or_404(Post, id=request.POST.get('post_id'))
#     is_liked = False
#     if post.likes.filter(id=request.user.id).exists():
#         post.likes.remove(request.user)
#         is_liked = False
#     else:
#         post.likes.add(request.user)
#         is_liked = True

#     context ={
#         'post': post,
#         'is_liked': is_liked,
#         'total_likes': post.likes.count(),
#     }
#     if request.is_ajax():
#         html = render_to_string('like_section.html.html', context, request=request)

#         return JsonResponse({'form': html})
#     return HttpResponseRedirect(post.get_absolute_url())

# def likes(request):
#     post = get_object_or_404(Post, id=request.POST.get('post_id'))
#     is_liked = False
#     if post.likes.filter(id=request.user.id).exists():
#         post.likes.remove(request.user)
#         is_liked = False
#     else:
#         post.likes.add(request.user)
#         is_liked = True
#     context ={
#         'post': post,
#         'is_liked': is_liked,
#         'total_likes': post.likes.count(),
#     }
#     if request.is_ajax():
#         html = render_to_string('like_section.html', context, request=request)
#         return JsonResponse({'form': html})

# @ login_required
# def likes(request):
#     if request.POST.get('action') == 'post':
#         result = ''
#         is_liked = ''
#         id = int(request.POST.get('postid'))
#         post = get_object_or_404(Post, id=id)
#         if post.likes.filter(id=request.user.id).exists():
#             post.likes.remove(request.user)
#             is_liked = 'False'
#             post.like_count -= 1
#             result = post.like_count
#             post.save()
#         else:
#             post.likes.add(request.user)
#             is_liked = 'True'
#             post.like_count += 1
#             result = post.like_count
#             post.save()
#         context={
#             'post': post,
#             'is_liked': is_liked,
#             'result': result,
#         }
#         if request.is_ajax():
#             return JsonResponse(context)

