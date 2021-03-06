
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from api.models import *
from trainerInterface.form import *
from trainerInterface.views import is_ajax


def dataTracking(request):
    request.session["href"] = '/dashboard/dataTracking/'
    session_id = request.GET.get('session_id', None)
    if session_id + "_selected_client" in request.session:
        currUserID = request.user.id
        groups = TrackingGroup.objects.filter(trainer__id__in=[1, currUserID])
    else:
        groups = None

    addGroupForm = GroupAddForm()
    addFieldForm = GroupFieldForm()
    return render(request, 'trainerInterface/dataTracking.html', {'groups': groups, 'addGroupForm':
                                                                  addGroupForm, 'addFieldForm': addFieldForm, 'selected_client': request.session[session_id+'_selected_client']})


def editGroup(request):

    if is_ajax(request):
        session_id = request.POST.get('session_id', None)
        groupId = request.POST.get('groupId', None)
        name = request.POST.get('name', None)
        fieldIds = json.loads(request.POST.get('fieldIds', None))['fieldIds']
        fieldnames = json.loads(request.POST.get(
            'fieldnames', None))["fieldnames"]
        fieldSelects = json.loads(request.POST.get(
            'classifications', None))["classifications"]
        toggles = json.loads(request.POST.get('toggles', None))["toggles"]

        editGroup = TrackingGroup.objects.get(id=groupId)
        editGroup.name = name
        editGroup.save()

        for id, fieldname, fieldselect, toggle in zip(fieldIds, fieldnames, fieldSelects, toggles):
            print(id)
            if not id:

                if fieldselect == 'text':
                    new_field = TrackingTextField(
                        name=fieldname,
                        type=False,
                    )
                else:
                    new_field = TrackingTextField(
                        name=fieldname,
                        type=True,
                    )

                if toggle == 'True':
                    new_field.save()
                    new_field.clientToggle.add(User.objects.get(
                        email=request.session[session_id + '_selected_client']))

                new_field.save()
                editGroup.textfields.add(new_field)
                editGroup.save()
            elif 'delete' in id:
                TrackingTextField.objects.get(id=id[0]).delete()

            else:
                editField = TrackingTextField.objects.get(id=id)
                editField.name = fieldname
                if toggle == 'True':
                    editField.clientToggle.add(User.objects.get(
                        email=request.session[session_id + '_selected_client']))
                else:
                    editField.clientToggle.remove(User.objects.get(
                        email=request.session[session_id + '_selected_client']))
                if fieldselect == 'text':
                    editField.type = False
                else:
                    editField.type = True
                editField.save()
                editGroup.textfields.add(editField)
                editGroup.save()

    return dataTracking(request)


def addGroup(request):

    if is_ajax(request):
        name = request.POST.get('name', None)
        session_id = request.POST.get('session_id', None)
        fieldnames = json.loads(request.POST.get(
            'fieldnames', None))["fieldnames"]
        fieldSelects = json.loads(request.POST.get(
            'classifications', None))["classifications"]
        toggles = json.loads(request.POST.get('toggles', None))["toggles"]
        print(fieldSelects)
        # try:

        new_group = TrackingGroup(
            name=name,
            trainer=request.user,
        )
        new_group.save()
        for fieldSelect, fieldname, toggle in zip(fieldSelects, fieldnames, toggles):
            if fieldSelect == "text":
                new_field = TrackingTextField(
                    name=fieldname,
                    type=False,
                )

                if toggle == 'True':
                    new_field.save()
                    new_field.clientToggle.add(User.objects.get(
                        email=request.session[session_id+'_selected_client']))

                new_field.save()
            else:

                new_field = TrackingTextField(
                    name=fieldname,
                    type=True,
                )

                if toggle == 'True':
                    new_field.save()
                    new_field.clientToggle.add(User.objects.get(
                        email=request.session[session_id+'_selected_client']))
                new_field.save()
            new_group.textfields.add(new_field)
            new_group.save()
            currUserID = request.user.id
            groups = TrackingGroup.objects.filter(
                trainer__id__in=[1, currUserID])

        print("saved")
        return render(request, 'trainerInterface/segments/newGroup.html', {'group': new_group, 'selected_client': request.session[session_id+'_selected_client'], 'length': len(groups)-1})

        # except:
        #     print("not saved")
        #     response = {
        #         'error': 'Error adding group'  # response message
        #     }
        #     return JsonResponse(response)


def toggleField(request):
    if is_ajax(request):
        id = request.POST.get('id', None)
        setting = request.POST.get('setting', None)
        session_id = request.POST.get('session_id', None)
        user = User.objects.get(email=request.session[session_id+'_selected_client'])
        field = TrackingTextField.objects.get(id=id)
        if setting == 'on':
            field.clientToggle.add(user)
            response = {
                'success': 'success'
            }
        elif setting == 'off':
            field.clientToggle.remove(user)
            response = {
                'success': 'success'
            }
        else:
            response = {
                'error': 'Could not toggle field!'
            }
        return JsonResponse(response)


def toggleGroup(request):
    if is_ajax(request):
        id = request.POST.get('id', None)
        setting = request.POST.get('setting', None)
        session_id = request.POST.get('session_id', None)
        user = User.objects.get(email=request.session[session_id+'_selected_client'])
        field = TrackingGroup.objects.get(id=id)
        if setting == 'on':
            field.clientToggle.add(user)
            response = {
                'success': 'success'
            }
        elif setting == 'off':
            field.clientToggle.remove(user)
            response = {
                'success': 'success'
            }
        else:
            response = {
                'error': 'Could not toggle field!'
            }
        return JsonResponse(response)