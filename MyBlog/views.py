from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from MyBlog.models import Article, User, Subscriber, Friend
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout, login
from django.shortcuts import redirect
from MyBlog.forms import EditForm
from MyBlog.forms import SubscriberForm
from django.core.mail import send_mail


def home(request, tag_slug=None):
    articles = Article.objects.all().order_by('-timestamp')
    tags = Article.objects.values_list('tags', flat=True)
    paginator = Paginator(articles, 3)  # 3 поста на странице
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        articles = paginator.page(paginator.num_pages)
    context = {
        'page': page,
        'articles': articles,
        'tags': tags
    }
    return render(request, 'blog/home.html', context)


def about(request):
    users = User.objects.all().order_by('username')
    context = {
        'users': users,
    }
    return render(request, 'blog/users.html', context)


def show_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'blog/article.html', {'article': article})


def delete(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        article.delete()
        return HttpResponseRedirect("/")
    except Article.DoesNotExist:
        return HttpResponseNotFound("<h2>Article not found</h2>")


def edit(request, article_id):

    try:
        article = Article.objects.get(id=article_id)
        form = EditForm(request.POST, instance=article)
        if request.method == "POST":
            article.title = request.POST.get("title")
            article.text = request.POST.get("text")
            article.preview = request.POST.get("preview")
            article.tags = request.POST.get("tags")
            article.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "blog/edit.html", {"form": form})
    except Article.DoesNotExist:
        return HttpResponseNotFound("<h2>Article not found</h2>")




def show_user(request, username):
    user_profile = get_object_or_404(User, username=username)
    articles = Article.objects.filter(user=user_profile)
    paginator = Paginator(articles, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    context = {
        'user_profile': user_profile,
        'articles': articles
    }
    return render(request, 'blog/user.html', context)


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "blog/register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('/')


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "blog/login.html"
    success_url = "/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class AddArticle(CreateView):
    model = Article
    fields = ['title', 'preview', 'text', 'tags']
    template_name = 'blog/add.html'
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddArticle, self).form_valid(form)


class AddFriend(CreateView):
    model = Friend
    fields = []
    template_name = 'blog/users.html'
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddFriend, self).form_valid(form)


def home_by_tag(request, tag):
    articles = Article.objects.filter(tags__name__in=[tag])
    paginator = Paginator(articles, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    context = {
        'page': page,
        'articles': articles,
        'tag': tag
    }
    return render(request, 'blog/tags.html', context)


def home_by_keyword(request):
    keyword = request.GET['keyword']
    articles = Article.objects.filter(text__icontains=keyword)
    paginator = Paginator(articles, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    context = {
        'page': page,
        'articles': articles,
        'keyword': keyword
    }
    return render(request, 'blog/search.html', context)


class Subscribe(CreateView):
    model = Subscriber
    fields = ['email']
    template_name = 'blog/subscribe_success.html'
    success_url = '/subscribe_success.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Subscribe, self).form_valid(form)


def show_users(request):
    users = User.objects.all().order_by('username')
    context = {
        'users': users,
    }
    return render(request, 'blog/users.html', context)


def show_friends(request):
    friends = Friend.objects.all().order_by('user.username')
    context = {
        'friends': friends
    }
    return render(request, 'blog/about.html', context)
