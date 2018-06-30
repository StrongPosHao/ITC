var tid         //删除单个的id
var tids = []   //批量删除的id
//全选&全不选
function checkChange(input){
    $('.table.table-hover.table-striped tbody td input').prop('checked',input.checked);
}

//此页面用于删除与批量删除
function singledelete(tagId){
    tid = tagId
    var info = "确定要删除选中的子标签吗?"
    $('.modal.fade .modal-body').text(info)
}
//批量删除
function batchdelete(){
    $(".table.table-hover.table-striped tbody td input:checked").each(function(index,ele){
        tids.push($(ele).parent().next().text())
    });
    var info = "确定要删除选中的子标签吗?"
    $('.modal.fade .modal-body').text(info)
}

//真正执行删除的那一步
function truedelete(){
    //此处需判断是单个删除还是批量删除
    if(tid){
        send_to_back(tid)
        toastr.success('删除成功!')
    }
    else if(tids){
        if(tids.length > 0){
            send_to_back2(tids)
        toastr.success('删除成功!')
        //一次请求之后及时清理数据
        tids = []
        }
    }
}

//向后台发送Ajax请求,删除单个
function send_to_back(tagId) {
    $.ajax({
        url: '/admin/tag/delete',
        type: 'POST',
        data: 'tagId=' + tagId,
        success: function (data) {
            window.location.reload();
        }
    });
}
//向后台发送Ajax请求,删除多个
function send_to_back2(tagIds) {
    $.ajax({
        url: '/admin/tag/batchdelete',
        type: 'POST',
        data: 'tagIds=' + tagIds,
        success: function (data) {
            window.location.reload();
        }
    });
}

