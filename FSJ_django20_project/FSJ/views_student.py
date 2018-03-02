from django.core.exceptions import PermissionDeniedfrom django.contrib.auth.decorators import login_required, user_passes_testfrom django.http import HttpResponsefrom django.template import loaderfrom django.shortcuts import redirectfrom .models import *from .utils import *from .forms import *# A test method to ensure a user is a Student to control access of certain views dependent on the user's classdef is_student(usr):    user = get_FSJ_user(usr)    if not isinstance(user, Student):        raise PermissionDenied    return True# The user class specific home page handler, which returns the appropriate page for this user class.# Contains the decordator to ensure the user is logged into the system and a test to ensure the user accessing the page is valid.@login_required@user_passes_test(is_student)def student_home(request, FSJ_user):    context = get_standard_context(FSJ_user)       template = loader.get_template("FSJ/student_home.html")    return HttpResponse(template.render(context, request))def student_awardslist(request, FSJ_user):    awards_list = Award.objects.filter(is_active = True)    template = loader.get_template("FSJ/student_awards_list.html")    context = get_standard_context(FSJ_user)    context["awards_list"] = awards_list    return HttpResponse(template.render(context,request))@login_required@user_passes_test(is_student)def student_addapplication(request, award_idnum):    FSJ_user = get_FSJ_user(request.user.username)        if request.method == "POST":        form = ApplicationRestrictedForm(request.POST)        if form.is_valid():            application = form.save(commit = False)            application.student = FSJ_user            application.award = Award.objects.get(awardid = award_idnum)            application.is_submitted = True                        application.save()            return redirect('home')    else:        # If the coordinator hasn't entered information yet, create a blank student form        form = ApplicationRestrictedForm()    context = get_standard_context(FSJ_user)    template = loader.get_template("FSJ/student_apply.html")    context["form"] = form    url = "/student_awardlist/" + award_idnum + "/apply/"    context["url"] = url        return HttpResponse(template.render(context, request))