$(document).ready(function(){
	$("#ScriptPoolFile").change(function(){
		$("#NativeFile").attr("disabled",true);
	});

	$("#NativeFile").change(function(){
		$("#ScriptPoolFile").attr("disabled",true);
	});
});


function set_scene(id)
{
    $("#NativeFile").attr("disabled",false);
    $("#ScriptPoolFile").attr("disabled",false);
    $("#add_activity_btn").attr("onclick","add_activity("+id+")");
    $(".tip").empty();
}

function set_activity(id)
{
    $("#rename_activity_btn").attr("onclick","rename_activity("+id+")");
}

function add_activity(scene_id)
{
	$(".tip").empty();
    if ($("#NativeFile").attr("disabled"))
    {
        $.ajax({
            type: "post",
            url: "/ves_ihep/add_activity/",
            data:
            {
                activity_name: $("#ActivityName").val(),
                scene_id: scene_id,
                script_id: $("#ScriptPoolFile option:selected").attr("id").split("_")[1],
                //script_type: $("#pool_type").val(),
                script_type: "pool"
            },
            dataType: "json",
            success: function(data)
            {
                if(data.result=="success")
                    location.reload()
                else{
                    str="Please make sure that you have choose suitable script file";
		    Tip(str);
		    }
            }
        });
    }
    else
    {
        $.ajaxFileUpload({
            type: "post",
            url: "/ves_ihep/add_activity/",
            fileElementId: "NativeFile",
            data:
            {
                activity_name: $("#ActivityName").val(),
                scene_id: scene_id,
                //script_type: $("#native_type").val(),
                script_type: "native"
            },
            dataType: "json",
            success: function(data)
            {
                if (data.result == "success")
                {
                    location.reload();
                }
                else
                {
		    str="Please make sure that you have choose suitable script file";
		    Tip(str);
		}
            },
            error: function(data)
            {
                console.info(data)
            }
        });
    }

}

function view_activity(activity_id)
{
    $.ajax({
        type: "post",
        url: "/ves_ihep/view_activity/",
        data:
        {
            activity_id:activity_id
        },
        dataType: "json",
        success: function(data)
        {
            if(data.result=="success")
                $("#script_content").html(data.content);
            else
                alert("error")
        }
    });
}

function delete_activity(activity_id)
{
    $.ajax({
        type: "post",
        url: "/ves_ihep/delete_activity/",
        data:
        {
            activity_id:activity_id
        },
        dataType: "json",
        success: function(data)
        {
            if(data.result=="success")
                location.reload()
            else
                alert("error")
        }
    });
}

function rename_activity(activity_id)
{
    $.ajax({
        type: "post",
        url: "/ves_ihep/rename_activity/",
        data:
        {
            activity_name:$('#Modified_Eva_Name').val(),
            activity_id:activity_id
        },
        dataType: "json",
        success: function(data)
        {
            if(data.result=="success")
                location.reload()
            else
                alert("error")
        }
    });
}

function deploy_init(scene_id)
{
    $('#deploy_list').empty()
    $('#deploy_activity_select').empty()
    $('#deploy_btn').attr("onclick","deploy("+scene_id+")")
    
    $.ajax({
        type: "post",
        url: "/ves_ihep/get_activity/",
        data:
        {
            scene_id:scene_id
        },
        dataType: "json",
        success: function(data)
        {
            if(data.result=="success")
                for(var key in data.activities)
                {
                    $('#deploy_activity_select').append('<option value="'+key+'" >'+data.activities[key]+'</option>')
                }
            else
		{
	            str="deploy scene failed";
		    Tip(str);
		}
        }
    });
}

function add_deploy_list()
{
    activity_id=$('#deploy_activity_select option:selected').val()
    activity_name=$('#deploy_activity_select option:selected').text()
    host_id=$('#Eva_Host option:selected').val()
    host_name=$('#Eva_Host option:selected').text()
    $(".tip").empty();
    $('#deploy_list').append('<tr id="deploy_list_'+activity_id+'_'+host_id+'">'+
            '<td id="deploy_activity_'+activity_id+'">'+activity_name+'</td>'+
            '<td id="deploy_host_'+host_id+'">'+host_name+'</td>'+
            '<td><button class="btn btn-default" onclick="delete_deploy_list('+activity_id+','+host_id+')">删除</button></td>'+
            '</tr>')
}

function delete_deploy_list(activity_id,host_id)
{
    $('#deploy_list_'+activity_id+'_'+host_id).remove()
}

/*function deploy(scene_id)
{
    var hosts=[]
    var activities=[]
    $('#deploy_list').children().each(function()
    {
        activity_id=$(this).attr('id').split('_')[2]
        host_id=$(this).attr('id').split('_')[3]
        hosts[String(activity_id)]=[]
        if(!IsContain(activities,activity_id))
            activities.push(activity_id)
    })
    $('#deploy_list').children().each(function()
    {
        activity_id=$(this).attr('id').split('_')[2]
        host_id=$(this).attr('id').split('_')[3]
        hosts[String(activity_id)].push(host_id)
    })
    $.ajax({
        type: "post",
        url: "/ves_ihep/deploy/",
        data:
        {
            scene_id:scene_id,
            activities:activities,
            hosts:hosts
        },
        dataType: "json",
        success: function(data)
        {
            if(data.result=="success")
                location.reload()
            else
                alert("error")
        }
    });
}*/

function deploy(scene_id)
{
    var hosts=[]
    var activities=[]
    $('#deploy_list').children().each(function()
    {
        activity_id=$(this).attr('id').split('_')[2]
        host_id=$(this).attr('id').split('_')[3]
        activities[String(host_id)]=[]
        if(!IsContain(hosts,host_id))
            hosts.push(host_id)
    })
    $('#deploy_list').children().each(function()
    {
        activity_id=$(this).attr('id').split('_')[2]
        host_id=$(this).attr('id').split('_')[3]
        activities[String(host_id)].push(activity_id)
    })
    $.ajax({
        type: "post",
        url: "/ves_ihep/deploy/",
        data:
        {
            scene_id:scene_id,
            activities:activities,
            hosts:hosts
        },
        dataType: "json",
        success: function(data)
        {
            if(data.result=="success")
                location.reload()
            else
                alert("error")
        }
    });
}

function IsContain(arr,value)
{
    for(var i=0;i<arr.length;i++)
    {
        if(arr[i]==value)
        return true;
    }
    return false;
}
$(function(){$('#Add_New_Action').on('show.bs.modal', function () {
  	$(".tip").empty();
	})
})
$(function(){$('#Deploy_Scene').on('show.bs.modal', function () {
  	$(".tip").empty();
	})
})
function Tip(tipcontent)
{
	$(".tip").append(tipcontent);
}
