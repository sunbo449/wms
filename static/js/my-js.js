 // 信息录入功能
 // 点击信息录入，日期默认为当日
 $('.reg-info').on('click', function () {
    var date = new Date();
    var y = date.getFullYear();
    var m = date.getMonth() + 1;
    var d = date.getDate();
    var timer = y + '/' + m + '/' + d;
    $('#out-data').prop('type', 'text').val(y + '/' + m + '/' + d);
})

// 如果修改日期，日期输入框聚焦事件，改为时间选择器；
$('#out-data').on('focus', function(){
    $(this).prop('type', 'date');
})

// 止错机制，点击提示
$('#reset').on('click', function(){
    var res = confirm('确定重新进行信息录入？')
    if (res === true){
        $(this).prop('type', 'reset');
    }
})
