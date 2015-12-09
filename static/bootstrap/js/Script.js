$(document).ready(function(){
    });

function delete_script(id)
{
    $.ajax({
        type: "post",
        url: "/ves_ihep/delete_script/",
        data:
        {
            script_id:id
        },
        dataType: "json",
        success: function(data)
        {
            if(data.result=="success")
                location.reload()
            else
                alert(error)
        }
    });
}
