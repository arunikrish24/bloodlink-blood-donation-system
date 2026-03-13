from django import forms
from .models import *

KERALA_DISTRICTS = [
    ('', 'Select'),
    ('alappuzha', 'Alappuzha'),
    ('ernakulam', 'Ernakulam'),
    ('idukki', 'Idukki'),
    ('kannur', 'Kannur'),
    ('kasaragod', 'Kasaragod'),
    ('kollam', 'Kollam'),
    ('kottayam', 'Kottayam'),
    ('kozhikode', 'Kozhikode'),
    ('malappuram', 'Malappuram'),
    ('palakkad', 'Palakkad'),
    ('pathanamthitta', 'Pathanamthitta'),
    ('thiruvananthapuram', 'Thiruvananthapuram'),
    ('thrissur', 'Thrissur'),
    ('wayanad', 'Wayanad'),
]

class LoginCreateForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm Password"
    )

    class Meta:
        model = Login
        fields = ["email"]
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["password1"])
        if commit:
            instance.save()
        return instance


class LoginUpdateForm(forms.ModelForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New Password", required=False
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm New Password", required=False
    )

    class Meta:
        model = Login
        fields = ["email"]
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("new_password1")
        p2 = cleaned.get("new_password2")
        if p1 or p2:
            if p1 != p2:
                self.add_error("new_password2", "New passwords do not match.")
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        p1 = self.cleaned_data.get("new_password1")
        if p1:
            instance.set_password(p1)
        if commit:
            instance.save()
        return instance


class LoginAuthForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class LocationForm(forms.ModelForm):
    district = forms.ChoiceField(
        choices=KERALA_DISTRICTS,
        label="Select District",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Location
        fields = ["state", "district", "city", "pincode", "address"]
        widgets = {
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class RCCForm(forms.ModelForm):
    class Meta:
        model = RCC
        fields = ["name", "phone"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BloodBankForm(forms.ModelForm):
    class Meta:
        model = BloodBank
        fields = ["name", "phone"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ["name", "blood_group", "last_donation_date", "phone"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'last_donation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BloodStockForm(forms.ModelForm):
    class Meta:
        model = BloodStock
        fields = [
            'a_positive', 'a_negative', 'b_positive', 'b_negative',
            'ab_positive', 'ab_negative', 'o_positive', 'o_negative',
            'threshold'
        ]
        widgets = {
            'a_positive': forms.NumberInput(attrs={'class': 'form-control'}),
            'a_negative': forms.NumberInput(attrs={'class': 'form-control'}),
            'b_positive': forms.NumberInput(attrs={'class': 'form-control'}),
            'b_negative': forms.NumberInput(attrs={'class': 'form-control'}),
            'ab_positive': forms.NumberInput(attrs={'class': 'form-control'}),
            'ab_negative': forms.NumberInput(attrs={'class': 'form-control'}),
            'o_positive': forms.NumberInput(attrs={'class': 'form-control'}),
            'o_negative': forms.NumberInput(attrs={'class': 'form-control'}),
            'threshold': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['blood_group', 'units_required', 'details']
        widgets = {
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'units_required': forms.NumberInput(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

class DonationForm(forms.Form):
    donor_id_input = forms.CharField(label="Donor ID", max_length=12, required=False)

    donor = forms.ModelChoiceField(
        queryset=Donor.objects.all(),
        empty_label="Select the donor"
    )

    blood_group = forms.CharField(
        label="Blood Group",
        required=False,
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
            'class': 'form-control'
        })
    )

    units_donated = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    remarks = forms.CharField(
        label="Remarks",
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Optional notes about the donation...'
        })
    )
