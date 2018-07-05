var aid         //删除单个的id
var aids = []   //批量删除的id
//全选&全不选
function checkChange(input){
    $('.table.table-hover.table-striped tbody td input').prop('checked',input.checked);
}

//此页面用于删除与批量删除
function singledelete(answerId){
    aid = answerId
    var info = "确定要删除选中的回答吗?"
    $('.modal.fade .modal-body').text(info)
}
//批量删除
function batchdelete(){
    $(".table.table-hover.table-striped tbody td input:checked").each(function(index,ele){
        aids.push($(ele).parent().next().text())
    });
    var info = "确定要删除选中的回答吗?"
    $('.modal.fade .modal-body').text(info)
}

//真正执行删除的那一步
function truedelete(){
    //此处需判断是单个删除还是批量删除
    if(aid){
        send_to_back(aid)
        toastr.success('删除成功!')
    }
    else if(aids){
        if(aids.length > 0){
            send_to_back2(aids)
        toastr.success('删除成功!')
        //一次请求之后及时清理数据
        aids = []
        }
    }
}

//向后台发送Ajax请求,删除单个
function send_to_back(answerId) {
    $.ajax({
        url: '/admin/answer/delete',
        type: 'POST',
        data: 'answerId=' + answerId,
        success: function (data) {
            window.location.reload();
        }
    });
}
//向后台发送Ajax请求,删除多个
function send_to_back2(answerIds) {
    $.ajax({
        url: '/admin/answer/batchdelete',
        type: 'POST',
        data: 'answerIds=' + answerIds,
        success: function (data) {
            window.location.reload();
        }
    });
}

//取消删除
function canceldelete_amswer(){
    aid = undefined
    aids = []
}


