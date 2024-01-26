from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import BlogPost


# Create your views here.

def home(request):

    posts = BlogPost.objects.all()

    return render(request, 'home.html',{'posts':posts})

def detail(request, postId):
    # pierwszy sposób
    # try:
    #     post = BlogPost.objects.get(id=postId)
    # except:
    #     raise Http404("This article does not exist")
    # 2 sposób
    post = get_object_or_404(BlogPost, id=postId)
    # [[1,'FIRST POST'], [2,'HELLOWORDL'], [3, 'THIRD POST']]
    if 'recently_read' in request.session:
        for (id, title) in request.session['recently_read']:
            if post.id == id:
                request.session['recently_read'].remove([id,title])
        request.session['recently_read'].insert(0,[post.id, post.title])
        if len(request.session['recently_read'])>4:
            request.session['recently_read'].pop()
    else:
        request.session['recently_read'] = [[post.id, post.title]]
    request.session.modified = True
    return render(request, 'detail.html',{'post':post, 'recently_read':request.session['recently_read'][1::]})
