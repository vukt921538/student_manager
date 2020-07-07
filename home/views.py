from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
@login_required
def home(request):
    posts = Post.objects.all().order_by('-date_published')
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.cleaned_data
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Đã đăng bài.')
        return redirect('home')

    else:
        form = PostForm(initial={
            'author': request.user
        })

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if page_number is None:
        page_number = 1

    post_pupular = Points.objects.all().order_by('-point')[:10]
    return render(request, 'home.html', context={
        'posts': posts,
        'form': form,
        'page_obj': page_obj,
        'range_page': paginator.page_range,
        'page_number': int(page_number),
        'post_popular': post_pupular
    })


# Like + 2, comment + 3
def post_detail(request, id):
    post_pupular = Points.objects.all().order_by('-point')[:10]
    post = Post.objects.get(pk=id)
    hidden_like = False
    hidden_dislike = False
    if request.user in post.like.all():
        hidden_like = True
    elif request.user in post.dislike.all():
        hidden_dislike = True
    comments = Comment.objects.filter(post=post)
    for comment in comments:
        comment.reply = Comment_to_comment.objects.filter(from_comment=comment)
    comment_form = CommentForm(initial={
        'user': request.user,
        'post': post,
    })
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.cleaned_data
            comment_form.save()
        return redirect('post_detail', post.id)

    request.session['post_id'] = post.id

    reply_comment = CtcForm(initial={
        'user': request.user,
    })
    return render(request, 'post.html', context={
        'post': post,
        'like_count': post.like.count(),
        'dislike_count': post.dislike.count(),
        'hidden_like': hidden_like,
        'hidden_dislike': hidden_dislike,
        'comments': comments,
        'comment_form': comment_form,
        'comment_to_comment_form': reply_comment,
        'post_popular': post_pupular
    })

def like_post(request, id):
    post = Post.objects.get(pk=id)
    try:
        p = Points.objects.get(post=post)
        p.point += 1
        p.save()
    except:
        Points.objects.create(
            post=post,
            point=1
        )
    if request.method == 'POST':
        if request.user in post.dislike.all():
            post.dislike.remove(request.user)
        post.like.add(request.user)
    return redirect('post_detail', post.id)

def dislike_post(request, id):
    post = Post.objects.get(pk=id)
    try:
        p = Points.objects.get(post=post)
        p.point -= 1
        p.save()
    except:
        Points.objects.create(
            post=post,
            point=-1
        )
    if request.method == 'POST':
        if request.user in post.like.all():
            post.like.remove(request.user)
        post.dislike.add(request.user)
    return redirect('post_detail', post.id)

def delete_post(request, id):
    post = Post.objects.get(pk=id)
    post.delete()
    return redirect('home')

def reply_comment(request, id):
    get_id_post = request.session.get('post_id', None)
    comment = Comment.objects.get(pk=id)
    cmt = request.POST.get('comment')
    if request.method == 'POST':
        Comment_to_comment.objects.create(
            user=request.user,
            from_comment=comment,
            comment=cmt
        )
    return redirect('post_detail', get_id_post)

def search_post(request):
    value = request.GET.get('data')
    page_obj = Post.objects.filter(title__icontains=value)
    print('RESULT: ', page_obj)
    post_pupular = Points.objects.all().order_by('-point')[:10]
    return render(request, 'home.html', context={
        'page_obj': page_obj,
        'value': value,
        'post_popular': post_pupular
    })