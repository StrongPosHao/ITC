var cid         //删除单个的id
var cids = []   //批量删除的id
//全选&全不选
function checkChange(input){
    $('.table.table-hover.table-striped tbody td input').prop('checked',input.checked);
}

//此页面用于删除与批量删除
function singledelete(categoryId){
    cid = categoryId
    var info = "确定要删除选中的标签分类吗?"
    console.debug($('#modal_del .modal-body'))
    $('#modal_del .modal-body').text(info)
}
//批量删除
function batchdelete(){
    $(".table.table-hover.table-striped tbody td input:checked").each(function(index,ele){
        cids.push($(ele).parent().next().text())
    });
    var info = "确定要删除选中的标签分类吗?"
    $('#modal_del .modal-body').text(info)
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
function send_to_back(categoryId) {
    $.ajax({
        url: '/admin/category/delete',
        type: 'POST',
        data: 'categoryId=' + categoryId,
        success: function (data) {
            window.location.reload();
        }
    });
}
//向后台发送Ajax请求,删除多个
function send_to_back2(categoryIds) {
    $.ajax({
        url: '/admin/category/batchdelete',
        type: 'POST',
        data: 'categoryIds=' + categoryIds,
        success: function (data) {
            window.location.reload();
        }
    });
}

//添加
function add(){
    console.debug($('#a-CATEGORY').val())
    console.debug($('#a-DESCRIPTION').val())
    var categoryName = $('#a-CATEGORY').val()
    var categoryDescription = $('#a-DESCRIPTION').val()
    send_to_back3(categoryName,categoryDescription)
    toastr.success("新增类别成功!")
    $('#a-CATEGORY').val("")
    $('#a-DESCRIPTION').val("")
}
//向后台发送Ajax请求,新增类别
function send_to_back3(categoryName,categoryDescription) {
    $.ajax({
        url: '/admin/category/add',
        type: 'POST',
        data: 'categoryName=' + categoryName + '&categoryDescription=' + categoryDescription,
        success: function (data) {
            window.location.reload();
        }
    });
}
var id
//编辑
function edit(categoryId,categoryName,categoryDescription){
    id = categoryId
    console.log(categoryId)
    console.log(categoryName)
    console.log(categoryDescription)
    $('#e-CATEGORY').val(categoryName)
    $('#e-DESCRIPTION').val(categoryDescription)
}
//确认编辑
function confirmEdit(){
    var categoryName = $('#e-CATEGORY').val()
    var categoryDescription = $('#e-DESCRIPTION').val()
    send_to_back4(id,categoryName,categoryDescription)
    toastr.success("修改类别成功!")
    $('#e-CATEGORY').val("")
    $('#e-DESCRIPTION').val("")
}
//向后台发送Ajax请求,修改类别
function send_to_back4(categoryId,categoryName,categoryDescription) {
    $.ajax({
        url: '/admin/category/edit',
        type: 'POST',
        data: 'categoryId=' + categoryId + '&categoryName=' + categoryName + '&categoryDescription=' + categoryDescription,
        success: function (data) {
            window.location.reload();
        }
    });
}
//取消删除
function canceldelete_category(){
    cid = undefined
    cids = []
}
