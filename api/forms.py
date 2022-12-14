from django import forms
from .models import user_info_data, follow
from django.contrib.auth.models import User


# 关注表单
class follow_form(forms.ModelForm):
    class Meta:
        model = follow
        fields = ('username', 'follow_city')


# 登录表单
class user_login_form(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


# 注册表单
class user_register_form(forms.ModelForm):
    # email = forms.EmailField(label="Email")
    # 验证两次密码是否相同
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email',)

    # def clean_[字段]这种写法Django会自动调用，来对单个字段的数据进行验证清洗。
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码不一致，请重新输入 ")


# 修改密码表单
class user_change_password_form(forms.ModelForm):
    old_password = forms.CharField()
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username',)

    # def clean_[字段]这种写法Django会自动调用，来对单个字段的数据进行验证清洗。
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码不一致，请重新输入 ")


# 用户信息表单
class user_info_form(forms.ModelForm):
    class Meta:
        model = user_info_data
        # 定义表单包含的字段
        fields = ('portrait',)


# 修改邮箱表单
class user_change_email_form(forms.ModelForm):
    class Meta:
        model = User
        # 定义表单包含的字段
        fields = ('email',)


# 粉丝列表
# class user_follow_form(forms.ModelForm):
#     class Meta:
#         model = Follow
#         fields = ('follow', 'fan', 'user')
