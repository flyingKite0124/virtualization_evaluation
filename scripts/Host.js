var loop=0
$(document).ready(function(){
       loop=setInterval(get_status,5000)
    });

function delete_host(id)
{
    $.ajax({
        type: "post",
        url: "/ves/delete_host/",
        data:
        {
            host_id:id
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

function get_status()
{
    $.ajax({
        type: "post",
        url: "/ves/get_status/",
        data: {},
        dataType: "json",
        success: function(data)
        {
            if(data.result=="success")
                for(var key in data.hosts)
                {
                    if(data.hosts[key]==0)
                        $("#host_connected_"+String(key)).html("Disconnected")
                    else if(data.hosts[key]==1)
                        $("#host_connected_"+String(key)).html("Connected")
                    else
                        $("#host_connected_"+String(key)).html("Running Script")
                }
            else
            {
                alert(error);
                clearInterval(loop);
            }
        }
    });
}
