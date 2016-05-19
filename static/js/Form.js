function ASFormCheck()
{
	EvaSecName=$("#EvaSecName").val();
	if(EvaSecName=="")
	{
		alert("Please enter the name of the scene");
		return false;	
	}
	else return true;

}

function AHFormCheck()
{
	EvaHost=$("#EvaHost").val();
	HostUser=$("#HostUser").val();
	HostPwd=$("#HostPwd").val();
	if(EvaHost=="")
	{
		alert("Please enter the ip of the host");
		return false;	
	}
	else if(HostUser=="")
	{
		alert("Please enter the name of the host user");
		return false;	
	}
	else if(HostPwd=="")
	{
		alert("Please enter the password of the host");
		return false;	
	}
	else return true;

}

function AScriptFormCheck()
{
	ScriptName=$("#ScriptName").val();
	if(ScriptName=="")
	{
		alert("Please enter the name of the script");
		return false;	
	}
	else return true;

}




