from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import permission_required

from .models import Article
from .forms import NewsPost


@permission_required('news.add_article')
def create_post(request):
    post = NewsPost(request.POST or None, request.FILES or None)
    if request.POST:
        if post.is_valid():
            instance = post.save(commit=False)
            instance.author = request.user
            instance.save()
            return HttpResponseRedirect(reverse('news:index'))
    context = {
        'post': post
    }
    return render(request, 'news/create_post.html', context)


def news_details(request, article_id, slug):
    article = get_object_or_404(Article, id=article_id)
    context = {
        'article': article
    }
    return render(request, 'news/detail.html', context)


def list_all(request):
    all_posts = Article.objects.all().order_by('-published_date')
    context = {
        'posts': all_posts,
    }
    return render(request, 'news/list.html', context)
