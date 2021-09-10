// 獲取現在的股票ID
var stock_id=$("#get_stock_id").text()

$('#post_stock_id').val(stock_id);
$(".goToMain").attr("href","/main/?stock_id="+stock_id);

$("#Kpic").css("background-image","url(../static/img/img_K/K_"+stock_id+".png)");
$("#Volume").css("background-image","url(../static/img/img_volume/volume_"+stock_id+".png)");
$("#Bollin").css("background-image","url(../static/img/img_bollin/bollin_"+stock_id+".png)");


$(".btn"+stock_id).removeClass("bg-custom-unimportent ");
$(".btn"+stock_id).removeClass("bd-custom-unimportent");

$(".btn"+stock_id).addClass("bg-custom-importent");
$(".btn"+stock_id).addClass("border");
$(".btn"+stock_id).addClass("border-secondary");

// 顯示庫存
function show_warehouse() {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var username = $("#username").text();
    console.log(csrf, username);
    $.ajax({
        type: 'POST',
        url: '/warehouse_table/',
        data: {
            "csrfmiddlewaretoken": csrf,
            "username": username
        },
        // contentType: "application/json",
        // dataType: 'application/json; charset=utf-8',

        //接收server端的回饋訊息result
        success: function (result) {
            console.log(result);
            $.each(result, function (name, value) { 
                if (name.length < 5){
                    $("#warehouse").append("<tr><td>" + name + " : " + value + "股</td><td>" +result['buy_' + name + '_price']+ "元</td></tr>")
                    // $("#warehouse").append("<td>" +result['buy_' + name + '_price']+ "元</td></tr>")
                }
            });

        },
        error: function (result) {
            console.log("回饋失敗");
        }
    })
};



// 顯示收益
function show_income() {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var username = $("#username").text();
    $.ajax({
        type: 'POST',
        url: '/income_table/',
        data: {
            "csrfmiddlewaretoken": csrf,
            "username": username
        },
        //---------------------------------------------------
        // contentType: "application/json",
        // dataType: 'application/json; charset=utf-8',

        //接收server端的回饋訊息result
        success: function (result) {
            console.log(result);
            $.each(result, function (name, value) {              
                $("#income").append("<tr><td>" + name + ".TW</td><td>" +value+"元</td></tr>")
            });

        },
        error: function (result) {
            console.log("回饋失敗");
        }
    })
};
show_warehouse();
show_income();

// setInterval("show_income()","5000");





