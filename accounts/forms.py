from django import forms


class UpdateProfile(forms.Form):

    next = forms.CharField(widget=forms.HiddenInput(), required=False)
    username = forms.CharField(label='Username')
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        detail_keys = kwargs.pop('detail_keys')
        next = kwargs.pop('next')

        super(UpdateProfile, self).__init__(*args, **kwargs)

        # set hidden next field
        self.fields['next'].initial = next

        # set inital values for the User model
        self.fields['username'].initial = user.username
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name

        # add fields and init values for the Profile model
        for detail_key in detail_keys:
            # add a field for this detail key
            self.fields[detail_key.key] = forms.CharField(label=detail_key.label)

            # add an initial value, if one is found in the user details
            if user.profile.details and detail_key.key in user.profile.details:
                self.fields[detail_key.key].initial = user.profile.details[detail_key.key]
