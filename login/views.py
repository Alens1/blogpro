import hashlib,os
from blogproject.settings import MEDIA_ROOT
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserForm, RegisterForm, UserProfileForm
from login import models
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
import uuid
from PIL import Image

# def login(request):
#     # 验证码图片生成
#     hashkey = CaptchaStore.generate_key()
#     imgage_url = captcha_image_url(hashkey)
#
#
#     if request.method == "POST":
#         username = request.POST.get('username', None)
#         password = request.POST.get('password', None)
#         vcode = request.POST.get('vcode')
#         vcode_key = request.POST.get('hashkey')
#         # 验证查询数据库生成正确的码
#         get_captcha = CaptchaStore.objects.get(hashkey=vcode_key)
#
#         message = "所有字段都必须填写！"
#         if username and password:  # 确保用户名和密码都不为空
#             username = username.strip()
#             # 用户名字符合法性验证
#             # 密码长度验证
#             # 更多的其它验证.....
#             try:
#                 user = models.User.objects.get(name=username)
#                 if user.password == password:
#                     if vcode.lower() == get_captcha.response:
#                         messages.add_message(request, messages.SUCCESS, '用户登录成功！', extra_tags='success')
#                         return redirect('/index')
#                     else:
#                         return render(request, 'login/login.html', locals())
#                 else:
#                     message = "密码不正确！"
#             except:
#                 message = "用户名不存在！"
#             return render(request, 'login/login.html', locals())
#     login_form = UserForm()
#     return render(request, 'login/login.html', locals())


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "密码错误！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_email'] = user.email
                    request.session['user_name'] = user.name
                    request.session['user_avatar'] = str(user.avatar)


                    #  headimage = user.avatar
                    # return render(request, 'blog/index.html', locals())
                    return redirect("/index")
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            #sex = register_form.cleaned_data['sex']
            # avatar = register_form.cleaned_data['avatar']

            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)  # 使用加密密码
                new_user.email = email
                #new_user.sex = sex
                # new_user.avatar = avatar
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    else:

        register_form = RegisterForm()
    print(register_form.errors)
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index")


def user_profile(request):

    return render(request, "login/profile.html")


def crop_image(file, uid):
    # 随机生成新的图片名，自定义路径。
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    cropped_avatar = os.path.join(uid, "avatar", file_name)
    # 相对根目录路径
    if not os.path.exists(os.path.join(MEDIA_ROOT,"avatars", uid, "avatar").replace('\\','/')):
        os.makedirs(os.path.join(MEDIA_ROOT,"avatars", uid, "avatar").replace('\\','/'))
    file_path = os.path.join(MEDIA_ROOT,"avatars", uid, "avatar", file_name).replace('\\','/')
    # 裁剪图片,压缩尺寸为200*200。
    img = Image.open(file)
    crop_im = img.resize((150, 150), Image.ANTIALIAS)
    crop_im.save(file_path)

    return cropped_avatar

def delete_old_image(old_avatar,uid):
    # 物理删除图片
    tu_jpg = os.path.join(MEDIA_ROOT,"avatars",str(uid),"avatar",str(old_avatar)).replace('\\','/')
    if os.path.isfile(tu_jpg):
        os.remove(tu_jpg)


@csrf_exempt
def user_edit(request):
    if request.method == "POST":
        userprofile_form = UserProfileForm(request.POST, request.FILES)
        message = "请检查填写的内容！"

        if userprofile_form.is_valid():  # 获取数据

            ava = request.FILES.get('avatar')  # 获取上传的文件，如果没有文件，则默认为None
            # if not myFile:
            #     return HttpResponse("no files for upload!")
            # destination = open(os.path.join(MEDIA_ROOT, user_directory_path), 'wb+')  # 打开特定的文件进行二进制的写操作
            # for chunk in myFile.chunks():  # 分块写入文件
            #     destination.write(chunk)
            # destination.close()
            user1 = models.User.objects.get(id = request.session.get("user_id"))
            old_avatar = user1.avatar
            delete_old_image(old_avatar,str(request.session.get('user_id')))
            cropped_avatar= crop_image(ava, str(request.session.get('user_id'))).replace('\\','/')

            username = userprofile_form.cleaned_data['username']
            birth = userprofile_form.cleaned_data['birth']
            phone = userprofile_form.cleaned_data['phone']
            # email = userprofile_form.cleaned_data['email']
            school = userprofile_form.cleaned_data['school']
            address = userprofile_form.cleaned_data['address']
            about = userprofile_form.cleaned_data['about']


            same_name_user = models.User.objects.filter(name=username)
            if same_name_user:  # 用户名唯一
                message = '用户已经存在，请重新选择用户名！'
            # same_email_user = models.User.objects.filter(email=email)
            # if same_email_user:  # 邮箱地址唯一
            #     message = '该邮箱地址已被注册，请使用别的邮箱！'
            same_phone_user = models.User.objects.filter(phone=phone)
            if same_phone_user:  # 手机号唯一
                message = '该手机号已被注册，请使用别的手机号！'

            # 当一切都OK的情况下，保存用户信息
            edit_user = models.User.objects.get(id=request.session.get('user_id'))
            edit_user.name = username
            # edit_user.email = email
            #new_user.sex = sex
            edit_user.avatar = str(cropped_avatar)
            edit_user.about=about
            edit_user.birth=birth
            edit_user.phone=phone
            edit_user.school=school
            edit_user.address=address
            edit_user.save()

            user = models.User.objects.get(id=request.session.get('user_id'))
            request.session['user_phone'] = user.phone
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            request.session['user_avatar'] = str(user.avatar)
            request.session['user_email'] = user.email
            request.session['user_address'] = user.address
            request.session['user_school'] = user.school
            request.session['user_about'] = user.about
            request.session['user_birth'] = user.birth



            return redirect('/profile/')  # 自动跳转到登录页面

    else:
        userprofile_form = UserProfileForm()
    print(userprofile_form.errors)
    return render(request, 'login/profile_edit.html', locals())




def hash_code(s, salt='mysite'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

