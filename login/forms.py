from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'input-item',
                                                                                          'placeholder': 'username'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'input-item',
                                                                                             'placeholder': 'username'}))
    # captcha = CaptchaField(label='验证码', widget=forms.TextInput(attrs={'class': 'input-item',
    #                                                                   'placeholder': '验证码'}))


class RegisterForm(forms.Form):

    
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'input-item',
                                                                                          'placeholder': 'username'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'placeholder': 'password',
                                                                                              'class': 'input-item'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'comfirm your password'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                          'placeholder': 'e-mail'}))
  #  sex = forms.ChoiceField(label='性别', choices=gender)
    # captcha = CaptchaField(label='验证码')

    # avatar = forms.FileField(label="头像")

class UserProfileForm(forms.Form):
    avatar = forms.FileField(label="头像")
    username = forms.CharField(label="用户名", max_length=128)
    birth = forms.DateField(label='日期', widget=forms.DateInput(attrs={'type':'date'}))
    phone = forms.CharField(max_length=11)
    school = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    about = forms.CharField(max_length=100)
    # email = forms.CharField(max_length=20)
    # gender = (
    #     ('male', '男'),
    #     ('female', '女'),
    # )
    # sex = forms.CharField(max_length=32, choices=gender)





    


