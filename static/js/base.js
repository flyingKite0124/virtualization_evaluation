 $(document).ready(function(){
	$('#Delete_Scene').on('show.bs.modal', function () {
		$.getJSON('/ves_ihep/show_scenes/',function(ret)
		{
			for(var i=0; i<ret.length; i++){
				$("#wait_to_be_del_scenes").append('<option value='+ret[i]+'>'+ret[i]+'</option>');
			}
		});
      //alert('嘿，我听说您喜欢模态框...');
  	});
});
