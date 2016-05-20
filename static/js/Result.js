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
            {
                showresult(data);
            }
            else
                alert("error")
        }
    });
}

function showresult(result)
{
    if(result.type==0)
    {
        document.getElementById("content").innerHTML=result.content;
    }
    else
    {
        var myChart = echarts.init(document.getElementById('content'));

        option = {
            title : {
                text: result.title
            },
            tooltip : {
                trigger: 'axis'
            },
            legend: {
                data: result.legend
            },
            calculable : true,
            xAxis : [
                {
                    name : result.xAxis.name,
                    type : 'category',
                    data : result.xAxis.data
                }
            ],
            yAxis : [
                {
                    name : result.yAxis.name,
                    type : 'value'
                }
            ],
            series : result.series
        };

        myChart.setOption(option);
    }
}