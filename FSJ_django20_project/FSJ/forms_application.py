from .models_application import Application
from django.forms import ModelForm

class ApplicationForm(ModelForm):

    class Meta:
        model = Application
        fields = ('award', 'student', 'is_submitted')
        
    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)   
        
        
class ApplicationRestrictedForm(ModelForm):
    
    class Meta:
        model = Application
        #fields = ('award', 'student', 'is_submitted')
        fields = ()
            
    def __init__(self, *args, **kwargs):
        super(ApplicationRestrictedForm, self).__init__(*args, **kwargs)
        #self.fields['award'].disabled=True
        #self.fields['student'].disabled=True 
        #self.fields['is_submitted'].disabled=True