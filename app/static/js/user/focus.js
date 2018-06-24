//点击关注与取消关注
function clickfocus(MyId,UserId){
    if($('#focus_'+UserId+" .btn").text() == '取消关注'){
        $('#focus_'+UserId+" .btn").text('关注他');
        toastr.info('取消关注作者成功');
        send_to_back(MyId,UserId,false);
        
    }else{
        $('#focus_'+UserId+" .btn").text('已关注');
        toastr.success('关注作者成功');
        send_to_back(MyId,UserId,true);
    }
    
}
//鼠标悬浮与移开
function movein(UserId){
    if($('#focus_'+UserId+" .btn").text() == '已关注'){
        $('#focus_'+UserId+" .btn").text('取消关注');
    }
}
function moveout(UserId){
    if($('#focus_'+UserId+" .btn").text() == '取消关注'){
        $('#focus_'+UserId+" .btn").text('已关注');
    }
}
//向后台发送Ajax请求
function send_to_back(MyId,UserId,isFocused) {
    $.ajax({
        url: '/XX',
        type: 'POST',
        data: 'MyId=' + MyId + '&UserId=' + UserId+'&isfocused='+isFocused,
        success: function (data) {
        }
    });
}