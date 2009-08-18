#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Zuza Software Foundation
#
# This file is part of Pootle.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from django.shortcuts import render_to_response
from django.http import HttpResponseForbidden
from django.template import RequestContext
from django.utils.translation import ugettext as _
from pootle.i18n.gettext import tr_lang
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from pootle_notifications.forms import LanguageNoticeForm, TransProjectNoticeForm
from pootle_notifications.models import Notices
from pootle_app.models import Language, TranslationProject
from pootle_app.models.permissions import get_matching_permissions
from pootle_app.models.profile import get_profile

def lang_notices(request, language_code):
    can_add = False
    can_view = False

    lang = Language.objects.get(code=language_code)
    if 'view' in get_matching_permissions(get_profile(request.user), lang.directory):
        can_view = True
    if request.user.is_authenticated() and 'administrate' in get_matching_permissions(get_profile(request.user), lang.directory):
        can_add = True

    if not can_add and not can_view:
        return HttpResponseForbidden()

    if can_view:
        content = Notices(content_object = lang)
        lang_notices =  Notices.objects.get_notices(content)[:5]

    if can_add:
        success = ""
        valid_form = False
        if request.method == 'POST': # If the form has been submitted...
            form = LanguageNoticeForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                # ...
                form.save()
                success = _("Notification sent.")
                valid_form = True
        if request.method == 'GET' or valid_form:
            form = LanguageNoticeForm() # An unbound form
            form.set_initial_value(language_code)

    template_vars = {
            "title"       :_('Add notice for %(language)s', {"language": tr_lang(lang.fullname)}),
            "back_link"   :language_code,
            "name"        :tr_lang(lang.fullname),
            }

    if can_add:
        template_vars["form"] = form
        template_vars["success"] = success

    if can_view:
        template_vars["notices"] = lang_notices

    return render_to_response('pootle_notifications/notices.html', template_vars,
            context_instance=RequestContext(request)  )

def transproj_notices(request, language_code, project_code):

    can_add = False
    can_view = False
    transproj = TranslationProject.objects.get(real_path = project_code + "/" + language_code)
    if 'view' in get_matching_permissions(get_profile(request.user), transproj.directory):
        can_view = True
    if request.user.is_authenticated() and 'administrate' in get_matching_permissions(get_profile(request.user), transproj.directory):
        can_add = True

    if not can_add and not can_view:
        return HttpResponseForbidden()

    if can_view:
        content = Notices(content_object = transproj)
        transproj_notices =  Notices.objects.get_notices(content)[:5]

    if can_add:
        success = ""
        valid_form = False
        if request.method == 'POST': # If the form has been submitted...
            form = TransProjectNoticeForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                # ...
                form.save()
                success = _("Notification sent.")
                valid_form = True
        if request.method == 'GET' or valid_form:
            form = TransProjectNoticeForm() # An unbound form
            form.set_initial_value(language_code, project_code)

    details = {"language": tr_lang(transproj.language.fullname), "project": transproj.project.fullname}
    template_vars = {
            "title" : _('Add notice for the project "%(project)s" in %(language)s', details),
            "back_link" : language_code+"/"+project_code,
            "name"      : _('"%(project)s" in %(language)s', details),
            }

    if can_add:
        template_vars["form"] = form
        template_vars["success"] = success

    if can_view:
        template_vars["notices"] = transproj_notices

    return render_to_response('pootle_notifications/notices.html', template_vars,
            context_instance=RequestContext(request)  )

@login_required
def view_notice_item(request, notice_id):
    notice_type = ContentType.objects.get_for_model(Notices)
    notice = notice_type.get_object_for_this_type(id=notice_id)
    template_vars = {
            "title" : _("View Notice"),
            "notice_message"  : notice.message,
            }

    return render_to_response('pootle_notifications/viewnotice.html', template_vars,
            context_instance=RequestContext(request)  )
