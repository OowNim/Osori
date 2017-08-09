from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def article_index(request):
    articles = Article.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    return render(request, 'board/index.html',{'articles' : articles})

def article_table(request):
    posts = Article.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    paginator = Paginator(posts, 10) # Show 25 articles per page

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    return render(request, 'board/test_board.html', {'articles': articles})

def article_detail(request, pk):
    articleses = Article.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    count = articleses.count()
    before = 0
    now = 0
    after = 0
    for a in range(0, count):
        if articleses[a].pk == int(pk):
            break

    now = articleses[a]
    if a > 0 :
        before = articleses[a-1]

    if a != count - 1:
        after = articleses[a+1]

    articles = [before, now, after]
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = now
            comment.save()
            return redirect('article_detail', pk=now.pk)
    else:
        form = CommentForm()
        now.view_count += 1
        now.save()
    return render(request, 'board/article_detail.html', {'articles' : articles})

@login_required
def article_new(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'board/article_edit.html', {'form': form})

@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'board/article_edit.html', {'form': form})

@login_required
def article_remove(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect('article_table')

def add_comment_to_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = CommentForm()
    return render(request, 'board/add_comment_to_article.html', {'form': form})

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('article_detail', pk=comment.article.pk)

