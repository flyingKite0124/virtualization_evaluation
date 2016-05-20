#!/usr/bin/python
#coding=utf-8

import os
import json
import datetime
import ves_connection
import fcntl
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound, HttpResponseNotAllowed
from ves_ihep.models import Scene, Script, Host, Activity, SceneHistory, ActivityHistory
from ves_ihep.forms import NewScene, DelScene
from django.core.serializers.json import DjangoJSONEncoder
from django.template import RequestContext, loader
# Create your views here.


def index(request):
    scene_list = Scene.objects.all()
    scripts = Script.objects.all()
    hosts = Host.objects.all()
    for scene in scene_list:
        scene.activities = Activity.objects.filter(scene=scene)
    context_dict = {'scenes': scene_list, 'scripts': scripts, 'hosts': hosts}
    return render(request, 'ves_ihep/index.html',context_dict)


def add_new_scene(request):
    if request.method == 'POST':
        form = NewScene(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/ves_ihep/')
        else:
            print form.errors
    else:
        return HttpResponseNotFound("Pelease Enter Right URL!")


def delete_scene(request):
    if request.method == 'POST':
        del_scene = Scene.objects.filter(name=request.POST['name'])
        if del_scene:
            del_scene.delete()
            return index(request)
        else:
            print "Not Select the deleted scene"
    else:
        return HttpResponseNotFound("Pelease Enter Right URL!")
    return HttpResponseRedirect("/ves_ihep/")


def show_scenes(request):
    scene_list = []
    if request.is_ajax():
        choices = Scene.objects.filter(stable=False)
        for choice in choices:
            scene_list.append(choice.name)
    return JsonResponse(scene_list, encoder=DjangoJSONEncoder, safe=False)


def hostpool(request):
    host_list = Host.objects.all()
    context_dict = {'hosts': host_list}

    return render(request, 'ves_ihep/hostpool.html', context_dict)


def add_host(request):
    if request.is_ajax() == False and request.method == 'POST':
        host = Host()
        host.IP = request.POST['IP']
        host.username = request.POST['username']
        host.passwd = request.POST['passwd']
        host.status = 0
        host.save()

        host_connect=ves_connection.connect.Host(host.IP,host.username,host.passwd)
        if not host_connect.test_connection():
            return HttpResponseRedirect('/ves_ihep/hostpool')
        if host_connect.init_host(host.id)!=host.id:
            host.delete()
        return HttpResponseRedirect('/ves_ihep/hostpool')


def get_status(request):
    if request.is_ajax() == True and request.method == "POST":
        ret = dict()
        ret['hosts'] = dict()
        hosts = Host.objects.all()
        for host in hosts:
            host_connect=ves_connection.connect.Host(host.IP,host.username,host.passwd)
            if host_connect.test_connection():
                ret['hosts'][host.id]=1
            else:
                ret['hosts'][host.id]=0
        ret['result'] = "success"
        return JsonResponse(ret)


def delete_host(request):
    if request.is_ajax() == True and request.method == "POST":
        Host.objects.get(pk=request.POST['host_id']).delete()
        return JsonResponse({'result': 'success'})



def scriptpool(request):
    script_list = Script.objects.filter(script_type="pool")
    for script in script_list:
        fp = open(script.script_path, "r")
        script.script_content = fp.read()
        fp.close()
    context_dict = {'scripts': script_list}

    return render(request, 'ves_ihep/scriptpool.html', context_dict)


def add_script(request):
    if request.method == "POST":
        script = Script()
        script.script_name = request.POST["ScriptName"]
        script.upload_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
        script.script_type = "pool"
        script.save()
        script.script_path = os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)),
            "scripts",
            "pool",
            str(script.id))
        script.save()
        with open(script.script_path, "w") as fp:
            fp.write(request.FILES['ScriptFile'].read())
    os.popen('dos2unix ' + script.script_path)
    return HttpResponseRedirect('/ves_ihep/scriptpool/')


def delete_script(request):
    if request.is_ajax() == True and request.method == "POST":
        script=Script.objects.get(pk=request.POST['script_id'])
        os.remove(script.script_path)
        script.delete()
        return JsonResponse({'result': 'success'})


def add_activity(request):
    if request.method == "POST":
        activity = Activity()
        activity.activity_name = request.POST['activity_name']
        activity.scene = Scene.objects.get(pk=request.POST['scene_id'])
        if request.POST['script_type'] == "pool":
            activity.script = Script.objects.get(pk=request.POST['script_id'])
        else:
            script = Script()
            script.upload_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
            script.script_name = str(
                script.upload_time) + request.FILES['Native_Act_File'].name
            script.script_type = "native"
            script.save()
            script.script_path = os.path.join(
                os.path.dirname(
                    os.path.dirname(__file__)),
                "scripts",
                "native",
                str(script.id))
            script.save()
            fp = open(script.script_path, "w")
            fp.write(request.FILES['Native_Act_File'].read())
            fp.close()
            os.popen('dos2unix ' + script.script_path)
            activity.script = Script.objects.get(pk=script.id)
        activity.save()
    return JsonResponse({'result': 'success'})


def view_activity(request):
    if request.is_ajax() == True and request.method == "POST":
        script = Activity.objects.get(pk=request.POST['activity_id']).script
        fp = open(script.script_path, "r")
        content = fp.read()
        fp.close()
        return JsonResponse({'result': 'success', 'content': content})


def delete_activity(request):
    if request.is_ajax() == True and request.method == "POST":
        act=Activity.objects.get(pk=request.POST['activity_id'])
        if act.script.script_type=="native":
            os.remove(act.script.script_path)
            act.script.delete()
        act.delete()
        return JsonResponse({'result': 'success'})


def rename_activity(request):
    if request.is_ajax() == True and request.method == "POST":
        activity = Activity.objects.get(pk=request.POST['activity_id'])
        activity.activity_name = request.POST['activity_name']
        activity.save()
        return JsonResponse({'result': 'success'})


def get_activity(request):
    if request.is_ajax() == True and request.method == "POST":
        _scene = Scene.objects.get(pk=request.POST['scene_id'])
        activities = Activity.objects.filter(scene=_scene)
        ret_activities = dict()
        for activity in activities:
            ret_activities[activity.id] = activity.activity_name
        return JsonResponse(
            {'result': 'success', 'activities': ret_activities})


def deploy(request):
    if request.is_ajax() == True and request.method == "POST":
        scene = Scene.objects.get(pk=request.POST['scene_id'])
        scene_history = SceneHistory()
        scene_history.scene = scene
        scene_history.save()
        run_count=int(request.POST['activity_count'])
        with open('/ves_server/tasks',"a") as fp:
            fcntl.flock(fp,fcntl.LOCK_EX)
            for run_id in range(run_count):
                run=request.POST.getlist('activities['+str(run_id)+'][]')
                host_id=int(run[0])
                activity_id=int(run[1])
                activity_history=ActivityHistory()
                activity_history.scene_history=scene_history
                activity_history.host=Host.objects.get(pk=host_id)
                activity_history.activity=Activity.objects.get(pk=activity_id)
                activity_history.save()
                activity_history.stdout_path = os.path.join(
                    os.path.dirname(
                        os.path.dirname(__file__)
                    ),
                    "result",
                    "stdout",
                    str(activity_history.id)
                )
                with open(activity_history.stdout_path,"w") as fout:
                    fout.write("script is running")
                activity_history.stderr_path = os.path.join(
                    os.path.dirname(
                        os.path.dirname(__file__)
                    ),
                    "result",
                    "stderr",
                    str(activity_history.id)
                )
                open(activity_history.stderr_path,"w").close()
                activity_history.save()

                activity=dict()
                activity["activity_history_id"]=activity_history.id
                activity["ip"]=activity_history.host.IP
                activity["script_path"]=activity_history.activity.script.script_path
                activity["script_name"]=os.path.basename(activity["script_path"])
                activity["stdout_path"]=activity_history.stdout_path
                activity["stderr_path"]=activity_history.stderr_path
                fp.writelines(json.dumps(activity)+"\n")

            fcntl.flock(fp,fcntl.LOCK_UN)
        return JsonResponse({'result': 'success'})



def view_result(request):
    if request.is_ajax() == True and request.method == "POST":
        activity_history = ActivityHistory.objects.get(
            pk=request.POST['activity_history_id'])
        with open(activity_history.stdout_path, "r") as fp:
            result = fp.read()
        return JsonResponse(
            {'result': 'success','type':0, 'content': result})


def evaresult(request):
    if request.is_ajax() == False and request.method == 'GET':
        template = loader.get_template('ves_ihep/EvaResult.html')
        temp_var = dict()
        temp_var['page'] = 'result'
        temp_var['scenes'] = Scene.objects.all()
        temp_var['scene_histories'] = SceneHistory.objects.all().order_by('-pk')
        for _scene_history in temp_var['scene_histories']:
            _scene_history.activity_histories = ActivityHistory.objects.filter(
                scene_history=_scene_history)
        context = RequestContext(request, temp_var)
        return HttpResponse(template.render(context))
    else:
        return HttpResponseNotAllowed(['GET'], 'illegal request')
