from django import forms
from .models import User

class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['email', 'password']
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('The email does not exist')
        
        user = User.objects.get(email=email)
        
        if not user.check_password(password):
            raise forms.ValidationError('The password is incorrect')
        
        return cleaned_data