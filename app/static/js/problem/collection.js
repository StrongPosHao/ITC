//收藏问题
function collect(userId, problemId) {
    console.debug($('.glyphicon.glyphicon-plus'));
    if ($('.glyphicon.glyphicon-plus').text() == '收藏') {
        $('.btn.plus-pro').css({ color: 'blue' });
        $('.glyphicon.glyphicon-plus').html('已收藏');
        send_to_back(userId, problemId, true);
    } else {
        $('.btn.plus-pro').css({ color: 'orange' });
        $('.glyphicon.glyphicon-plus').html('收藏');
        send_to_back(userId, problemId, false);
    }
}

//向后台发送Ajax请求

function send_to_back(userId, problemId, ischecked) {
    $.ajax({
        url: '/XX',
        type: 'POST',
        data: 'userId=' + userId + '&problemId=' + problemId + '&ischecked' + ischecked,
        success: function (data) {
        }
    });
}