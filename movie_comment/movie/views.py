from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import movie_info, movie_comments
from .forms import SearchForm

# Create your views here.

def index(request):
    """テスト用のクラスです"""
    movie_list = movie_info.objects.all().order_by('-movie_update')
    context = {'movie_list' : movie_list}
    return render(request, 'movie/index.html', context)


def comments(request, m_id):
    """テスト用のクラスです"""
    movie = movie_info.objects.get(movie_id=m_id)
    real_id = movie.id
    real_name = movie.movie_title
    com_list = movie_comments.objects.filter(movie_info_id=real_id)
    context = {'com_list' : com_list, 'm_name' : real_name}
    return render(request, 'movie/comment.html', context)
    #return HttpResponse("映画ID：%s" % real_id)

def detail(request, m_id):
    """テスト用のクラスです"""
    m_title = movie_info.objects.get(movie_id=m_id)
    return HttpResponse("映画：%s" % m_title.movie_title)

def comment_search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            keyword = form.cleaned_data.get("keyword")
            if keyword:
                comments_list = movie_comments.objects.filter(comment_text__icontains=keyword)
                name_list = []
                for comment in comments_list:
                    #name_list.append(movie_info.objects.filter(id=comment.movie_info_id).movie_title)
                    name_list.append(comment.comment_text + "    --- <<" + movie_info.objects.get(id=comment.movie_info_id).movie_title + ">>")
                    #name_list.append("comment")
                #return render(request, 'movie/ajax.html', {'form':form, 'comments_list': comments_list})
                return render(request, 'movie/ajax.html', {'form':form, 'comments_list': name_list})
    else:
        form = SearchForm()
    return render(request, 'movie/ajax.html', {'form':form, 'comments_list': False})

def ajax_search(request):
    if request.method == 'GET':
        data = {}
        keyword = request.GET.get('keyword', None)
        if keyword:
            count = movie_comments.objects.filter(comment_text__icontains=keyword).count()
            data = {"count": count}
            return JsonResponse(data)
        else:
            data = {"count": "No result"}
            return JsonResponse(data)