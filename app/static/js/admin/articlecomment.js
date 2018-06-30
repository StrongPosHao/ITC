var cid         //删除单个的id
var cids = []   //批量删除的id
//全选&全不选
function checkChange(input){
    $('.table.table-hover.table-striped tbody td input').prop('checked',input.checked);
}

//此页面用于删除与批量删除
function singledelete(commentId){
    cid = commentId
    var info = "确定要删除选中的评论吗?"
    $('.modal.fade .modal-body').text(info)
}
//批量删除
function batchdelete(){
    $(".table.table-hover.table-striped tbody td input:checked").each(function(index,ele){
        cids.push($(ele).parent().next().text())
    });
    var info = "确定要删除选中的评论吗?"
    $('.modal.fade .modal-body').text(info)
}

//真正执行删除的那一步
function truedelete(){
    //此处需判断是单个删除还是批量删除
    if(cid){
        send_to_back(cid)
        toastr.success('删除成功!')
    }
    else if(cids){
        if(cids.length > 0){
            send_to_back2(cids)
        toastr.success('删除成功!')
        //一次请求之后及时清理数据
        cids = []
        }
    }
}

//向后台发送Ajax请求,删除单个
function send_to_back(commentId) {
    $.ajax({
        url: '/admin/articlecomment/delete',
        type: 'POST',
        data: 'commentId=' + commentId,
        success: function (data) {
            window.location.reload();
        }
    });
}
//向后台发送Ajax请求,删除多个
function send_to_back2(commentIds) {
    $.ajax({
        url: '/admin/articlecomment/batchdelete',
        type: 'POST',
        data: 'commentIds=' + commentIds,
        success: function (data) {
            window.location.reload();
        }
    });
}

