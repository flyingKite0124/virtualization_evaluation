 $(document).ready(function(){
  $("#Add_C_Acti").click(function(){ 
		$("#NativeFile").attr("disabled",false);
		$("#ScriptPoolFile").attr("disabled",false);
		$("#Cpu").append('<li style="border-bottom:white solid thin;"><a href="#">&nbsp;•'+"UNKnow"+"</a></li>");			 		   

	});		

	
  $("#Add_M_Acti").click(function(){ 

	$("#Mem").append('<li style="border-bottom:white solid thin;"><a href="#">&nbsp;•'+"UNKnow"+"</a></li>");			 		   

	});		
	
  $("#Add_N_Acti").click(function(){ 

	$("#Net").append('<li style="border-bottom:white solid thin;"><a href="#">&nbsp;•'+"UNKnow"+"</a></li>");			 		   

	});		
	
  	$(".rm_acti").click(function(){
  		$("#CPU_1").remove();
  	});
  	

	$("#ScriptPoolFile").change(function(){

		$("#NativeFile").attr("disabled",true);
	});

	$("#NativeFile").change(function(){

		$("#ScriptPoolFile").attr("disabled",true);
	});
	
	$('#Delete_Scene').on('show.bs.modal', function () {
		$.getJSON('/ves_ihep/show_scenes/',function(ret)
		{
			for(var i=0; i<ret.length; i++){
				$("#wait_to_be_del_scenes").append('<option value='+ret[i]+'>'+ret[i]+'</option>');
			}
		});
      //alert('嘿，我听说您喜欢模态框...');
  	});

  	//$("#delete_scen").click(function(){
  	//	$("#"+).remove();
  	//})

});
