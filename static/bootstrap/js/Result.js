$(document).ready(function(){
});


function view_script(activity_id)
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
                $("#content").html(data.content);
            else
                alert("error")
        }
    });
}

function view_result(activity_history_id)
{
    $.ajax({
        type: "post",
        url: "/ves_ihep/view_result/",
        data:
        {
            activity_history_id:activity_history_id
        },
        dataType: "json",
        success: function(data)
        {
            if(data.result=="success")
                $("#content").html(data.content);
            else
                alert("error")
        }
    });
}
