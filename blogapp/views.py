import json
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from .models import Post, Comment
from .forms import PostForm, CommentForm
from itertools import chain

def explore(request):
    posts = Post.objects.order_by('-id')
    comment_form = CommentForm()
    return render(request, 'explore.html', {'posts' : posts, 'comment_form' : comment_form})

def post_list(request):
    if request.user.is_authenticated:       
        followings = request.user.followings.all()
        followings = chain(followings, [request.user])
        posts = Post.objects.filter(author__in=followings).order_by('-id')
        comment_form = CommentForm()
        return render(request, 'main.html', {'posts' : posts, 'comment_form' : comment_form})
    else:
        return render(request,'signin.html')

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            messages.info(request, "새 글이 등록되었습니다.")
            return redirect('/')
    else:
        form = PostForm()
    return render(request, 'new_post.html', {'form':form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    if post.author != request.user:
        messages.warning(request, '잘못된 접근입니다.')
        return redirect('/')

    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        post = Post.objects.get(pk=post_id)
        form = PostForm(instance=post)
        return render(request, 'edit_post.html',{'post' : post, 'form' : form})

@login_required
def delete(request, post_id):
    post = Post.objects.get(pk = post_id)
    if post.author != request.user:
        messages.warning(request, '잘못된 접근입니다.')
        return redirect('/')
    else:
        post.delete()
        messages.success(request, '삭제완료')
        return redirect('/')

@login_required
@require_POST
def post_like(request):
    pk = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=pk)
    post_like, post_like_created = post.like_set.get_or_create(user=request.user)

    if not post_like_created:
        post_like.delete()
        message = "좋아요 취소"
    else:
        message = "좋아요"

    
    context = {'like_count' : post.like_count, 
                'message' : message,
                'username' : request.user.username
             }

    return HttpResponse(json.dumps(context), content_type="text/json-comment-filtered")

@require_POST
def comment_create(request, post_id):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_id
        comment.save()
    
    return redirect('/')

@require_http_methods(['GET', 'POST'])
def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return redirect('/')
    comment.delete()
    return redirect('/')
