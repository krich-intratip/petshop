from django.shortcuts import render, get_object_or_404
from .models import Post 


def home(request):
    all_posts = Post.objects.all()

    context = {
        'all_posts': all_posts,
    }

    return render(request, 'blog/home.html', context)


def post_detail(request, slug):

    single_post = get_object_or_404(Post, slug=slug)

    recent_articles = (
        Post.objects.exclude(id=single_post.id)  
        .order_by('-date_updated')[:3]  
    )

    context = {
        'single_post': single_post,
        'recent_articles': recent_articles,
    }
    return render(request, 'blog/blog-detail.html', context)



