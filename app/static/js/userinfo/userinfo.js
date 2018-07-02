window.onload =(function() {
        $("#nav_6").addClass("active");
        $("#nav_2,#nav_3,#nav_4,#nav_5,#nav_1").removeClass("active");

});



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