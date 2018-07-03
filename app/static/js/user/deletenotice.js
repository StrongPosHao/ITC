// 1  toastr.success('提交数据成功');
// 2  toastr.error('Error');
// 3  toastr.warning('只能选择一行进行编辑');
// 4  toastr.info('info');
function deletenotice(noticeId,userId){
    toastr.success('删除通知成功!');
    sendDeleteNotice(noticeId,userId);
}
function canceldeletenotice(){
    toastr.info('取消删除通知!');
}
//向后台发送Ajax请求
function sendDeleteNotice(noticeId,userId) {
    $.ajax({
        url: '/XX',
        type: 'POST',
        data: 'noticeId=' + noticeId + '&userId=' + userId,
        success: function (data) {
        }
    });
}