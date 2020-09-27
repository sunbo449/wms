from django import forms
from django.core.validators import RegexValidator  # 调用进行正则校验
from django.core.exceptions import ValidationError  # 抛出错误信息
from account import models
from utils.md5 import encrypt


class RegisterForm(forms.ModelForm):
    """用户注册表单"""
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(
        r"^[1](([3][0-9])|([4][5-9])|([5][0-3,5-9])|([6][5,6])|([7][0-8])|([8][0-9])|([9][1,8,9]))[0-9]{8}$",
        '手机号格式错误')], error_messages={'unique': '手机号已经注册'})
    password = forms.CharField(label='密码', min_length=6, max_length=16, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='重复密码', min_length=6, max_length=16, widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ['username', 'mobile_phone', 'role', 'team', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off',
            })

    # 用户名验证
    def clean_username(self):
        username = self.cleaned_data['username']

        if not username:
            raise ValidationError('用户名不能为空！')
        return username

    # 手机号验证
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.UserProfile.objects.filter(mobile_phone=mobile_phone).exists()

        if not mobile_phone:
            raise ValidationError('手机号不能为空！')
        return mobile_phone

    # 角色验证
    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role == "":
            raise ValidationError('用户角色不能为空！')
        return role
    
    # 组别验证
    def clean_team(self):
        team = self.cleaned_data.get('team')
        if team == "":
            raise ValidationError('用户组别不能为空!')
        return team

    # 加密密码 (如果不加密，存储在数据库中的密码是明文的，容易撞库，泄露密码。我们使用md5加密处理)
    def clean_password(self):
        pwd = self.cleaned_data['password']
        return encrypt(pwd)

    # 密码验证
    def clean_confirm_password(self):
        pwd = self.cleaned_data['password']
        confirm_password = encrypt(self.cleaned_data.get('confirm_password'))

        if pwd != confirm_password:
            raise ValidationError('两次密码输入不一致')
        return confirm_password

