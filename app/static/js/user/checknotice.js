function checknotice(noticeId,userId){
    toastr.info('您已查看该通知!');
    $('.red-point').attr('class','');
    sendCheckNotice(noticeId,userId);
}
//向后台发送Ajax请求
function sendCheckNotice(noticeId,userId) {
    $.ajax({
        url: '/XX',
        type: 'POST',
        data: 'noticeId=' + noticeId + '&userId=' + userId,
        success: function (data) {
        }
    });
}