var stock_id=$("#get_stock_id").text();
console.log('ok');
$("#History_pic").css("background-image","url(../static/img/img_history/history_"+stock_id+".png)");
$('#Prophet_pic').css("background-image","url(../static/img/img_prophet/prophet_"+stock_id+".png)");


$(".btn"+stock_id).removeClass("bg-custom-unimportent ");
$(".btn"+stock_id).removeClass("bd-custom-unimportent");

$(".btn"+stock_id).addClass("bg-custom-importent");
$(".btn"+stock_id).addClass("border");
$(".btn"+stock_id).addClass("border-secondary");

// 顯示日期
function  GetDateStr(AddDayCount) { 
    var  dd =  new  Date();
    dd.setDate(dd.getDate()+AddDayCount); //获取AddDayCount天后的日期
    var  y = dd.getFullYear(); 
    var  m = (dd.getMonth()+1)<10? "0" +(dd.getMonth()+1):(dd.getMonth()+1); //获取当前月份的日期，不足10补0
    var  d = dd.getDate()<10? "0" +dd.getDate():dd.getDate(); //获取当前几号，不足10补0
    return  m+ "/" +d; 
}


// 顯示未來股價
function future_price() {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var username = $("#username").text();
    var stock_id = $("#get_stock_id").text();
    $.ajax({
        type: 'POST',
        url: '/future/',
        data: {
            "csrfmiddlewaretoken": csrf,
            "username": username,
            "stock_id": stock_id
        },
        //---------------------------------------------------
        // contentType: "application/json",
        // dataType: 'application/json; charset=utf-8',

        //接收server端的回饋訊息result
        success: function (result) {
            console.log(typeof(result["1"]));
            for(i=1; i<11; i++){
                // $('.predict'+i.toString()).text("Day"+i.toString()+":"+result[i.toString()])
                $('.predict'+i.toString()).text(GetDateStr(i)+" : "+result[i.toString()])
            }
            
        },
        error: function (result) {
            console.log("回饋失敗");
        }
    })
};

function future_range_lower() {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var username = $("#username").text();
    var stock_id = $("#get_stock_id").text();
    $.ajax({
        type: 'POST',
        url: '/range_lower/',
        data: {
            "csrfmiddlewaretoken": csrf,
            "username": username,
            "stock_id": stock_id
        },
        //---------------------------------------------------
        // contentType: "application/json",
        // dataType: 'application/json; charset=utf-8',

        //接收server端的回饋訊息result
        success: function (result) {
            console.log(result);
            // console.log(typeof(result));
            for(i=1; i<11; i++){
                $('.range'+i.toString()).text(result[i.toString()])
            }
            
        },
        error: function (result) {
            console.log("回饋失敗");
        }
    })
};

function future_range_upper() {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var username = $("#username").text();
    var stock_id = $("#get_stock_id").text();
    $.ajax({
        type: 'POST',
        url: '/range_upper/',
        data: {
            "csrfmiddlewaretoken": csrf,
            "username": username,
            "stock_id": stock_id
        },
        //---------------------------------------------------
        // contentType: "application/json",
        // dataType: 'application/json; charset=utf-8',

        //接收server端的回饋訊息result
        success: function (result) {
            console.log(result);
            
            for(i=1; i<11; i++){
                var origin = $('.range'+i.toString()).text()
                $('.range'+i.toString()).text(origin+"~"+"Day"+i.toString()+"~"+result[i.toString()])
            }
            
        },
        error: function (result) {
            console.log("回饋失敗");
        }
    })
};

future_price();
future_range_lower();
// future_range_upper();


setTimeout('future_range_upper()','100');




if (stock_id == 2330){
    console.log('catch');
    $('.reason1').html('<b>理由1</b>:<br>蘋果即將推出新iPhone,<br> 第三季營收看俏')
    $('.reason2').html('<b>理由2</b>:<br>英特爾宣布跨足GPU市場,<br> 搶佔TSMC未來3奈米產能')
} else {
    console.log("noCATCH")
}

if (stock_id == 2454){
    console.log('catch');
    $('.reason1').html('<b>理由1</b>:<br>天璣2000即將推出,<br> 美系外資加碼評等')
    $('.reason2').html('<b>理由2</b>:<br>7月營收403.6億元,<br> 年增51.2%')
} else {
    console.log("noCATCH")
}

if (stock_id == 2317){
    console.log('catch');
    $('.reason1').html('<b>理由1</b>:<br>鴻海股價回神,<br> 站上5日均線')
    $('.reason2').html('<b>理由2</b>:<br>秋季蘋果推出新品,<br> H2營收可期')
} else {
    console.log("noCATCH")
}

if (stock_id == 2303){
    console.log('catch');
    $('.reason1').html('<b>理由1</b>:<br>聯電產能滿載,<br> 但需求續旺無法滿足市場需求, 毛利率明年拚突破4成')
    $('.reason2').html('<b>理由2</b>:<br>7月營收183.66億元,<br> 年增18.53%')
} else {
    console.log("noCATCH")
}

if (stock_id == 2308){
    console.log('catch');
    $('.reason1').html('<b>理由1</b>:<br>台達電上半年EPS 5.46元,<br> 預計全年賺超過1個股本')
    $('.reason2').html('<b>理由2</b>:<br>進入電動車時代,<br> 身為全球充電設備龍頭製造商, 獲利可望續強')
} else {
    console.log("noCATCH")
}

if (stock_id == 2881){
    console.log('catch');
    $('.reason1').html('<b>理由1</b>:<br>富邦金預計2022年完成合併日盛金<br>作業, 為近年少數成功金金併案例')
    $('.reason2').html('<b>理由2</b>:<br>金控EPS王, 獲利年年成長<br>, 有望續發股票')
} else {
    console.log("noCATCH")
}

if (stock_id == 1303){
    console.log('catch');
    $('.reason1').html('<b>理由1</b>:<br>南亞7月營收367.97億,<br> 年增69.16%')
    $('.reason2').html('<b>理由2</b>:<br>台塑四寶持續交出好成績,<br> 全球需求復甦, H1 EPS高達5.13元')
} else {
    console.log("noCATCH")
}

if (stock_id == 1301){
    console.log('catch');
    $('.reason1').html('<b>理由1</b>:<br>台塑7月營收223.44億,<br> 年增42.17%')
    $('.reason2').html('<b>理由2</b>:<br>塑膠股目標價上修,<br> 全球需求復甦, H1 EPS高達5.53元')
} else {
    console.log("noCATCH")
}

if (stock_id == 2882){
    console.log('catch');
    $('.reason1').html('<b>理由1</b>:<br>國泰金前七月賺千億,<br> 較去年同期大幅成長120%')
    $('.reason2').html('<b>理由2</b>:<br>7月為台股股利發放旺季,<br> 國壽7月股利收入約進帳43億元')
} else {
    console.log("noCATCH")
}

if (stock_id == 2412){
    console.log('catch');
    $('.reason1').html('<b>理由1</b>:<br>近期台股震盪走低,<br> 抗跌首選電信類股')
    $('.reason2').html('<b>理由2</b>:<br>中華電將開發三重土地,<br> 持續活化資產, 多角化經營')
} else {
    console.log("noCATCH")
}