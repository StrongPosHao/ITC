//收藏问题
function collect(userId, problemId) {
    console.debug($('.glyphicon.glyphicon-plus'));
    if ($('.glyphicon.glyphicon-plus').text() == '收藏') {
        $('.btn.plus-pro').css({ color: 'blue' });
        $('.glyphicon.glyphicon-plus').html('已收藏');
        toastr.success('收藏成功!');
        sendCollection(userId, problemId, true);
    } else {
        $('.btn.plus-pro').css({ color: 'orange' });
        $('.glyphicon.glyphicon-plus').html('收藏');
        toastr.info('取消收藏!');
        sendCollection(userId, problemId, false);
    }
}

//向后台发送Ajax请求

function sendCollection(userId, problemId, ischecked) {
    $.ajax({
        url: '/question/favorite',
        type: 'POST',
        data: 'userId=' + userId + '&problemId=' + problemId + '&ischecked=' + ischecked,
        success: function (data) {
        }
    });
}