var uid         //删除单个的id
var uids = []   //批量删除的id
var unames = []   //批量删除的name
//全选&全不选
function checkChange(input){
    $('.table.table-hover.table-striped tbody td input').prop('checked',input.checked);
}

//此页面用于删除与批量删除
function singledelete(userId,username){
    uid = userId
    var info = "确定要删除用户:[ "+username+" ]吗?"
    $('.modal.fade .modal-body').text(info)
}
//批量删除
function batchdelete(){
    $(".table.table-hover.table-striped tbody td input:checked").each(function(index,ele){
        //console.debug($(ele).parent().next().next().text())
        uids.push($(ele).parent().next().text())
        unames.push($(ele).parent().next().next().text())
    });
    var info = "确定要删除用户:[ "
    for(j = 0; j < unames.length; j++) {
        info = info + unames[j] + ','
    }
    info=info.substring(0,info.length-1)
    info = info + " ]吗?"
    $('.modal.fade .modal-body').text(info)
}

//真正执行删除的那一步
function truedelete(){
    console.debug("uid:"+uid)
    console.debug("uids:"+uids)
    //此处需判断是单个删除还是批量删除
    if(uid){
        send_to_back8(uid)
        toastr.success('删除成功!')
    }
    else if(uids){
        if(uids.length > 0){
            send_to_back9(uids)
        toastr.success('删除成功!')
        //一次请求之后及时清理数据
        uids = []
        unames = []
        }
    }
}

//向后台发送Ajax请求,删除单个
function send_to_back8(userId) {
    $.ajax({
        url: '/admin/user/delete',
        type: 'POST',
        data: 'userId=' + userId,
        success: function (data) {
            window.location.reload();
        }
    });
}
//向后台发送Ajax请求,删除多个
function send_to_back9(userIds) {
    $.ajax({
        url: '/admin/user/batchdelete',
        type: 'POST',
        data: 'userIds=' + userIds,
        success: function (data) {
            window.location.reload();
        }
    });
}

