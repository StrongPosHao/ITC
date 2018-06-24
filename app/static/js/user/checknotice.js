function checknotice(noticeId,userId){
    toastr.info('您已查看该通知!');
    $('.red-point').attr('class','');
    send_to_back(noticeId,userId);
}
//向后台发送Ajax请求
function send_to_back(noticeId,userId) {
    $.ajax({
        url: '/XX',
        type: 'POST',
        data: 'noticeId=' + noticeId + '&userId=' + userId,
        success: function (data) {
        }
    });
}