from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponse
from django.template import loader 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import gettext_lazy as _
from .tokens import account_activation_token
from .forms import *
from .models import *
from .utils import *
from .views_student import *
from .views_adjudicator import *
from .views_coordinator import *
from django.conf import settings
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

# A method used to redirect users who have no path to bring them to their home page
def redirect_to_home(request):
    return home(request)

# Handles the generations of a unique link to the account activation page and emails this
# link to the provided email address. 
def registration(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if User.objects.filter(email = data['email']).exists():
                user = User.objects.get(email = data['email'])
                if user.last_login is None:
                    current_site=get_current_site(request)
                    mail_subject = _('[DO NOT REPLY] Activate Campus Saint Jean Awards Account')
                    message = loader.render_to_string('registration/register_email.html', {
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                        'token': account_activation_token.make_token(user)
                        })
                    to_email = data['email']
                    email = EmailMessage(mail_subject, message, to=[to_email])
                    email.send()  
                    template = loader.get_template("registration/register_email_sent.html")
                    return HttpResponse(template.render())
                else:
                    template = loader.get_template("registration/already_active.html")
                    return HttpResponse(template.render())
            else:
                messages.error(request, 'placeholder')
    else:
        form = SignupForm()
    return render(request,'registration/register_form.html', {'form':form})

# Landing page after following the link generated by registration.
# calls SetPasswordForm to set the users password for the first time.
def register_activation(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User.objects.get(pk=uid)
    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            return redirect('login')
    else:
        form = SetPasswordForm(user)
    return render(request,'registration/register_activation.html', {'form':form})

# The home page, split out depending on what class of user is requested.
# Contains the decordator to ensure the user is logged into the system.
@login_required
def home(request):
    FSJ_user = get_FSJ_user(request.user.username)
    if isinstance(FSJ_user, Student):
        return redirect('student_awardslist')
    elif isinstance(FSJ_user, Coordinator):
        return redirect('coord_awardslist')
    elif isinstance(FSJ_user, Adjudicator):
        return redirect('adj_awardslist')
    elif request.user.is_superuser:
        return redirect('/admin/')
    else:
        return non_FSJ_home(request)

# The profile view for the user accessing their own profile (with restricted field editting)
# Includes a POST handler for saving based on the results from the form, and adds the form back to the same template if validation fails
# Contains the decorator to ensure the user is logged into the system and a test to ensure the user accessing the page is valid.
@login_required
@user_passes_test(is_FSJ_user)
def profile(request):
    FSJ_user = get_FSJ_user(request.user.username)
    # Save the profile data if the request is a POST
    if request.method == "POST":
        if isinstance(FSJ_user, Student):
            profile_form = StudentRestrictedForm(request.POST, instance=FSJ_user)
        elif isinstance(FSJ_user, Adjudicator):
            profile_form = AdjudicatorRestrictedForm(request.POST, instance=FSJ_user)
        elif isinstance(FSJ_user, Coordinator):
            profile_form = CoordinatorRestrictedForm(request.POST, instance=FSJ_user)
        # If the from is valid, save it and redirect as a GET (POST, REDIRECT, GET).
        # If the form isn't valid we'll rerender it with the errors to display on the template
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')

    else:
        # On a GET, we prefill the fields based on the instance of the user whose profile is being editted
        if isinstance(FSJ_user, Student):
            profile_form = StudentRestrictedForm(instance=FSJ_user)
        elif isinstance(FSJ_user, Adjudicator):
            profile_form = AdjudicatorRestrictedForm(instance=FSJ_user)
        elif isinstance(FSJ_user, Coordinator):
            profile_form = CoordinatorRestrictedForm(instance=FSJ_user)        
            
    # Add the form as well as this URL to the context, since the template is used for other handlers as well (for Coordinators to update other users' profiles)
    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/profile.html")
    context["form"] = profile_form
    url = "/profile/"
    context["url"] = url
    context["return_url"] = "/FSJ/"
    return HttpResponse(template.render(context, request))

@login_required
@user_passes_test(is_coordinator)
def awards(request):
    FSJ_user = get_FSJ_user(request.user.username)
    return coordinator_awards(request, FSJ_user)

@login_required
@user_passes_test(is_coordinator)
def committees(request):
    FSJ_user = get_FSJ_user(request.user.username)
    return coordinator_committeeslist(request, FSJ_user)

@login_required
@user_passes_test(is_coordinator)
def years(request):
    FSJ_user = get_FSJ_user(request.user.username)
    return coordinator_yearslist(request, FSJ_user)

# A generic template that allows non FSJ Users who manage to log in to see a system message to see the coordinator to be set up properly
# Also allows the admin to access the admin page.
@login_required
def non_FSJ_home(request):
    # The FSJ User class does not have many of the features of its children classes and can act as a stand-alone model with default language preference.
    # The FSJ User in this case is not saved so behaves transiently
    FSJ_user = FSJUser()
    context = get_standard_context(FSJ_user)   
    template = loader.get_template("FSJ/non_FSJ_home.html")
    return HttpResponse(template.render(context, request))

@login_required
@user_passes_test(is_coordinator_or_adjudicator)
def view_student(request):
    student_ccid = request.GET.get("ccid","")
    awardid = request.GET.get("awardid","")
    return_url = request.GET.get("return", "")
    
    FSJ_user = get_FSJ_user(request.user.username)
    try:
        student = Student.objects.get(ccid = student_ccid)
    except Student.DoesNotExist:
        raise Http404(_("Student does not exist"))
    
    # load a form with the student's info
    form = StudentReadOnlyForm(instance=student)
    
    context = get_standard_context(FSJ_user)
    context["student"] = student
    context["form"] = form
    
    url_is_safe = is_safe_url(url=urllib.parse.unquote(return_url),
                            allowed_hosts=settings.ALLOWED_HOSTS,
                            require_https=request.is_secure(),)
    if url_is_safe and return_url:    
        context["return_url"] = str(return_url)
    template = loader.get_template("FSJ/view_student.html")
    return HttpResponse(template.render(context, request))    

@login_required
@user_passes_test(is_coordinator_or_adjudicator)
def view_application(request):
    FSJ_user = get_FSJ_user(request.user.username)
    if isinstance(FSJ_user, Coordinator):
        return coordinator_view_application(request)
    elif isinstance(FSJ_user, Coordinator):
        return adjudicator_view_application(request)