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
    $('#modal_del .modal-body').text(info)
}
//批量删除
function batchdelete(){
    $(".table.table-hover.table-striped tbody td input:checked").each(function(index,ele){
        tids.push($(ele).parent().next().text())
    });
    var info = "确定要删除选中的子标签吗?"
    $('#modal_del .modal-body').text(info)
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

//添加
function add(){
    console.debug($('#a-CATEGORY').val())
    console.debug($('#a-DESCRIPTION').val())
    var tagName = $('#a-CATEGORY').val()
    var tagDescription = $('#a-DESCRIPTION').val()
    send_to_back3(tagName,tagDescription)
    toastr.success("新增类别成功!")
    $('#a-CATEGORY').val("")
    $('#a-DESCRIPTION').val("")
}
//向后台发送Ajax请求,新增类别
function send_to_back3(tagName,tagDescription) {
    $.ajax({
        url: '/admin/tag/add',
        type: 'POST',
        data: 'tagName=' + tagName + '&tagDescription=' + tagDescription,
        success: function (data) {
            window.location.reload();
        }
    });
}
var id
//编辑
function edit(tagId,tagName,tagDescription){
    id = tagId
    console.log(tagId)
    console.log(tagName)
    console.log(tagDescription)
    $('#e-CATEGORY').val(tagName)
    $('#e-DESCRIPTION').val(tagDescription)
}
//确认编辑
function confirmEdit(){
    var tagName = $('#e-CATEGORY').val()
    var tagDescription = $('#e-DESCRIPTION').val()
    send_to_back4(id,tagName,tagDescription)
    toastr.success("修改类别成功!")
    $('#e-CATEGORY').val("")
    $('#e-DESCRIPTION').val("")
}
//向后台发送Ajax请求,修改类别
function send_to_back4(tagId,tagName,tagDescription) {
    $.ajax({
        url: '/admin/tag/edit',
        type: 'POST',
        data: 'tagId=' + tagId + '&tagName=' + tagName + '&tagDescription=' + tagDescription,
        success: function (data) {
            window.location.reload();
        }
    });
}
