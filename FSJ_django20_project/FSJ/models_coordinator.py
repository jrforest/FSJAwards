from django.db import modelsfrom .models_FSJUser import FSJUserfrom django.utils.translation import gettext_lazy as _from django.forms import *class Coordinator(FSJUser):    def user_class(self):        return "Coordinator"    