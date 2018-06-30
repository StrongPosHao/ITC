function listTag(articleId){
    console.debug(articleId)
    send_to_back(articleId)

}
//向后台发送Ajax请求,删除多个
function send_to_back(articleId) {
    $.ajax({
        url: '/admin/articletag',
        type: 'POST',
        data: 'articleId=' + articleId,
        success: function (data) {
            console.debug(data)
        }
    });
}