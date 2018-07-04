var aid         //删除单个的id
var aids = []   //批量删除的id
//全选&全不选
function checkChange(input){
    $('.table.table-hover.table-striped tbody td input').prop('checked',input.checked);
}

//此页面用于删除与批量删除
function singledelete(articleId){
    aid = articleId
    var info = "确定要删除选中的文章吗?"
    $('.modal.fade .modal-body').text(info)
}
//批量删除
function batchdelete(){
    $(".table.table-hover.table-striped tbody td input:checked").each(function(index,ele){
        aids.push($(ele).parent().next().text())
    });
    var info = "确定要删除选中的文章吗?"
    $('.modal.fade .modal-body').text(info)
}

//真正执行删除的那一步
function truedelete(){
    //此处需判断是单个删除还是批量删除
    if(aid){
        send_to_back_article(aid)
        toastr.success('删除成功!')
    }
    else if(aids){
        if(aids.length > 0){
            send_to_back2_article(aids)
        toastr.success('删除成功!')
        //一次请求之后及时清理数据
        aids = []
        }
    }
}

//向后台发送Ajax请求,删除单个
function send_to_back_article(articleId) {
    $.ajax({
        url: '/admin/article/delete',
        type: 'POST',
        data: 'articleId=' + articleId,
        success: function (data) {
            window.location.reload();
        }
    });
}
//向后台发送Ajax请求,删除多个
function send_to_back2_article(articleIds) {
    $.ajax({
        url: '/admin/article/batchdelete',
        type: 'POST',
        data: 'articleIds=' + articleIds,
        success: function (data) {
            window.location.reload();
        }
    });
}

//取消删除
function canceldelete_article(){
    aid = undefined
    aids = []
}


