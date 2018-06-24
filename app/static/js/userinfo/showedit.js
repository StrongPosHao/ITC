//悬浮文字上显示修改
function showEdit(title,userId){
    console.debug($('#'+title+'_'+userId));
    $('#'+title+'_'+userId).css({visibility:'visible'});
}

//点击修改显示表单
function showForm(title,userId){
    console.debug($('#'+title+'_div_'+userId));
    $('#'+title+'_div_'+userId).css({display: 'inline'});
    $('#'+title+'_p_'+userId).css({display: 'none'});
}