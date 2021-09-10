update_price()
// 10秒更新一次即時股價
function update_price(){
    // console.log("更新");
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var stock_id = $("#get_stock_id").text()
    console.log(stock_id)
    $.ajax({
        type: 'POST',
        url: '/now_price/',
        data: {
            csrfmiddlewaretoken: csrf,
            stock_id:stock_id
        },
        //接收server端的回饋訊息result
        success: function (result) {
            // console.log(typeof(result));
            $('#now_price').val(result);
            $('.now_price').text(result+'元');

        },
        error: function (result) {
            console.log("回饋失敗"+result);
        }
    })
}

setInterval("update_price()","10000");