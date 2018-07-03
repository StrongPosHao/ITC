//标签的收藏与取消收藏
function cut(title,tagId,userId){
    if(title == '取消收藏'){
        $('#favorite-btn-'+tagId).attr('title','收藏该标签');
        $('#favorite-btn-'+tagId).attr('onclick','cut("收藏该标签", ' + tagId + ',' + userId + ');');
        $('#favorite-btn-' + tagId + ' span').attr('class','glyphicon glyphicon-plus-sign');
        toastr.success('取消收藏标签!');
        send_to_back(userId,tagId,false);
    }
    if(title == '收藏该标签'){
        $('#favorite-btn-'+tagId).attr('title','取消收藏');
        $('#favorite-btn-'+tagId).attr('onclick','cut("取消收藏", ' + tagId + ',' + userId + ');');
        $('#favorite-btn-' + tagId + ' span').attr('class','glyphicon glyphicon-minus-sign');
        toastr.info('收藏标签成功!');
        send_to_back(userId,tagId,true);
    }
}
//向后台发送Ajax请求
function send_to_back(userId,tagId,iscollected) {
    $.ajax({
        url: '/user/choose-tag',
        type: 'POST',
        data: 'userId=' + userId + '&tagId=' + tagId + '&iscollected=' + iscollected,
        success: function (data) {
        }
    });
}