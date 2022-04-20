from django.db import models







class User(models.Model):
    '''用户表'''

    # gender = (
    #     ('male', '男'),
    #     ('female', '女'),
    # )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    # sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128, unique=True)
    birth = models.CharField(max_length=100, blank=True, default="unkonwn")
    phone = models.CharField(max_length=100, blank=True)
    school = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    # upload_to 指定上传文件位置 上传头像
    # 这里指定存放在avatars/ 目录下
    avatar = models.FileField(upload_to='avatar', blank=True)
    about = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


# class ProfileUser(models.Model):
#     name = models.CharField(max_length=128, unique=True)
#     birth = models.CharField(max_length=100, blank= True, default="konw")
#     phone = models.CharField(max_length=100, blank=True)
#     school = models.CharField(max_length=100, blank=True)
#     address = models.CharField(max_length=100, blank=True)
#     # upload_to 指定上传文件位置 上传头像
#     # 这里指定存放在avatars/ 目录下
#     about = models.TextField(blank=True)



    
