$(function(){$('#Add_Scene').on('show.bs.modal', function () {
  	$(".tip").empty();
	})
})
$(function(){$('#Add_Host').on('show.bs.modal', function () {
  	$(".tip").empty();
	})
})
$(function(){$('#Add_Script').on('show.bs.modal', function () {
  	$(".tip").empty();
	})
})

function ASFormCheck()
{
	$(".tip").empty();	
	EvaSecName=$("#EvaSecName").val();
	if(EvaSecName=="")
	{
		str="Please enter the name of the scene";
		Tip(str);
		return false;	
	}
	else return true;

}

function AHFormCheck()
{
	$(".tip").empty();
	EvaHost=$("#EvaHost").val();
	HostUser=$("#HostUser").val();
	HostPwd=$("#HostPwd").val();
	if(EvaHost=="")
	{
		str="Please enter the ip of the host";
		Tip(str);
		return false;	
	}
	else if(HostUser=="")
	{
		str="Please enter the name of the host user";
		Tip(str);
		return false;	
	}
	else if(HostPwd=="")
	{
		str="Please enter the password of the host";
		Tip(str);
		return false;	
	}
	else return true;

}

function AScriptFormCheck()
{
	$(".tip").empty();
	ScriptName=$("#ScriptName").val();
	if(ScriptName=="")
	{
		str="Please enter the name of the script";
		Tip(str);
		return false;	
	}
	else return true;

}

function Tip(tipcontent)
{
	$(".tip").append(tipcontent);
}


