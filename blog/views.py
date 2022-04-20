from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Tag
from login.models import User
from .forms import ArticlePostForm
from django.views.generic import ListView, DetailView
from pure_pagination.mixins import PaginationMixin
from django.contrib import messages
import markdown
from django.views.decorators.csrf import csrf_exempt
import uuid,os
from PIL import Image
from blogproject.settings import MEDIA_ROOT


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    context_object_name = 'post_list'
    paginate_by = 10
    return render(request, 'blog/index.html', context={'post_list': post_list})



class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        return super().get_queryset().filter(created_time__year=year, created_time__month=month)


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(IndexView):
    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get("pk"))
        return super().get_queryset().filter(tags=t)


class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        id = kwargs['pk']
        post = Post.objects.get(id = str(id))
        pic = post.picture
        request.session['post_pic'] = str(pic)
        response = super().get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response


def search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q)  )

    return render(request, 'blog/index.html', {'post_list': post_list})



def crop_image(file, pid):
    # 随机生成新的图片名，自定义路径。
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    cropped_avatar = os.path.join(pid, "picture", file_name)
    # 相对根目录路径

    if not os.path.exists(os.path.join(MEDIA_ROOT, "picture", pid, "picture").replace('\\', '/')):
        os.makedirs(os.path.join(MEDIA_ROOT, "picture", pid, "picture").replace('\\', '/'))
    file_path = os.path.join(MEDIA_ROOT, "picture", pid, "picture", file_name).replace('\\', '/')
    # 裁剪图片,压缩尺寸为200*200。
    img = Image.open(file)
    crop_im = img.resize((1000, 500), Image.ANTIALIAS)
    crop_im.save(file_path)

    return cropped_avatar


@csrf_exempt
def post_create(request):
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        # data=request.POST.copy()
        # author = User.objects.get(name = request.session.get('user_name'))
        # data.update({'author': author})
        # data.update({'tags': None})
        article_post_form = ArticlePostForm(request.POST,request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():


            title = article_post_form.cleaned_data['title']
            body = article_post_form.cleaned_data['body']
            # excerpt = article_post_form.cleaned_data['excerpt']
            category = article_post_form.cleaned_data['category']
            picture = article_post_form.cleaned_data['picture']

            tag = request.POST.get('tags')
            user__id = request.session.get('user_id')         #session get 到的只是一个属性而不是一个实例！
            author = User.objects.get(id = user__id)  #注意这里是name=user_name,而不能直接写入user_name


            pic = crop_image(picture,str(user__id))

            new_article = Post(title=title, body=body,
                               category=category,picture=str(pic),
                               author=author)
            new_article.save()
            post_id = new_article.id

            post_pic = Post.objects.get(id=post_id)
            post_pic11 = post_pic.picture
            request.session['post_picture']=str(post_pic11)

            new_article.tags.add(tag)
            # 将新文章保存到数据库中
            new_article.save()
            # 完成后返回文章列表
            return redirect("/index/")
        # 如果熟不不合法，返回错误信息
        else:
            print(article_post_form.errors)
            messages.add_message(request, messages.ERROR, '填写信息不完整或有误，请检查后在确认！', extra_tags='danger')
            return render(request, 'blog/create.html',locals())
        # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
    # 返回模板
    return render(request, 'blog/create.html',locals())
