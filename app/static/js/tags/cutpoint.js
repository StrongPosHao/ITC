//标签的收藏与取消收藏
function cut(title,tagId,userId){
    if(title == '取消收藏'){
        $('.btn.collect-btn').attr('title','收藏该标签');
        $('.btn.collect-btn').attr('onclick','cut("收藏该标签",1,1);');
        $('.btn.collect-btn span').attr('class','glyphicon glyphicon-plus-sign');
        send_to_back(userId,tagId,false);
    }
    if(title == '收藏该标签'){
        $('.btn.collect-btn').attr('title','取消收藏');
        $('.btn.collect-btn').attr('onclick','cut("取消收藏",1,1);');
        $('.btn.collect-btn span').attr('class','glyphicon glyphicon-minus-sign');
        send_to_back(userId,tagId,true);
    }
}
//向后台发送Ajax请求
function send_to_back(userId,tagId,iscollected) {
    $.ajax({
        url: '/XX',
        type: 'POST',
        data: 'userId=' + userId + '&tagId=' + tagId + '&iscollected' + iscollected,
        success: function (data) {
        }
    });
}