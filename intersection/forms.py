from django import forms
from api.models import user_info_data


# 用户信息表单
class user_info_form(forms.ModelForm):
    class Meta:
        model = user_info_data
        # 定义表单包含的字段
        fields = ('phone', 'portrait')