from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from article.models import Article, Category, Comment, Message
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import ContactUsForm, MessageForm
from django.views.generic.base import View, TemplateView, RedirectView
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView, ArchiveIndexView, YearArchiveView
from .models import Article
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import CustomLoginRequiredMixin


# def article_detail(request, slug, id=None):
#     article = get_object_or_404(Article, slug=slug, id=id)
#     if request.method == 'POST':
#         parent_id = request.POST.get('parent_id')
#         body = request.POST.get('body')
#         Comment.objects.create(body=body, article=article, user=request.user, parent_id=parent_id)
#     return render(request, "article/article_detail.html", {'article': article})


def article_list(request):
    articles = Article.objects.all()
    page_number = request.GET.get('page')
    paginator = Paginator(articles, 1)
    try:
        objects_list = paginator.page(page_number)
    except PageNotAnInteger:
        objects_list = paginator.page(1)
    except EmptyPage:
        raise Http404("صفحه مورد نظر پیدا نشد")
    return render(request, 'article/article_list.html', {'articles': objects_list})


def category_detail(request, pk=None):
    category = get_object_or_404(Category, id=pk)
    articles = category.articles.all()
    return render(request, "article/article_list.html", {'articles': articles})


def search(request):
    q = request.GET.get('q')
    articles = Article.objects.filter(title__icontains=q)
    page_number = request.GET.get('page')
    paginator = Paginator(articles, 1)
    try:
        objects_list = paginator.page(page_number)
    except PageNotAnInteger:
        objects_list = paginator.page(1)
    except EmptyPage:
        raise Http404("صفحه مورد نظر پیدا نشد")
    return render(request, "article/article_list.html", {'articles': objects_list})


def contactus(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # title = form.cleaned_data['title']
            # text = form.cleaned_data['text']
            # email = form.cleaned_data['email']
            # Message.objects.create(title=title, text=text, email=email)
            # instance = form.save(commit=False)
            # instance.age += 5
            # instance.save()
            form.save()

    else:
        form = MessageForm()
    return render(request, "article/contact_us.html", {'form': form})


class HomePageRedirect(RedirectView):
    # url = "/articles/list"
    pattern_name = 'article:article_detail'
    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        # print(self.request.user.username)
        return super().get_redirect_url(*args, **kwargs)


class ArticleList(TemplateView):
    pass
    # template_name = 'article/article_list2.html'
    #
    #
    # def get_context_data(self, **kwargs):
    # context = super().get_context_data(**kwargs)
    # context['object_list'] = Article.objects.all()
    # return context


class UserList(ListView):
    queryset = User.objects.all()
    template_name = 'article/user_list.html'


class ArticleDetailView(CustomLoginRequiredMixin, DetailView):
    model = Article

    def post(self, request, *args, **kwargs):
        Comment.objects.create(body=request.POST.get('body'), article=self.get_object(), user=request.user,
                               parent_id=request.POST.get('parent_id'))
        return redirect(self.get_object().get_absolute_url())


class ArticleListView(CustomLoginRequiredMixin ,ListView):
    # model = Article
    context_object_name = 'articles'
    paginate_by = 1
    queryset = Article.objects.filter(published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Atusa'
        return context


class ContactUsView(FormView):
    template_name = 'article/contact_us.html'
    form_class = MessageForm
    success_url = reverse_lazy('home:main')

    def form_valid(self, form):
        form_data = form.cleaned_data
        Message.objects.create(**form_data)

        return super().form_valid(form)



class MessageView(CustomLoginRequiredMixin, CreateView):
    model = Message
    fields = ('title', 'text')
    success_url = reverse_lazy('article:message_list')



    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.email = self.request.user.email
        instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        print(self.object.title)
        return super(MessageView, self).get_success_url()


class MessageListView(ListView):
    model = Message


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message_list'] = Message.objects.filter(email=self.request.user.email)
        return context

class MessageUpdateView(UpdateView):
    model = Message
    fields = ('title', 'text')
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('article:message_list')



class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('article:message_list')



class ArchiveIndexArticleView(ArchiveIndexView):
    model = Article
    date_field = 'updated'


class YearArchiveArticleView(YearArchiveView):
    model = Article
    date_field = 'pub_date'
    make_object_list = True
    allow_future = True
























