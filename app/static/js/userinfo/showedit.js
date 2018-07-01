//悬浮文字上显示修改
function showEdit(title,userId){
    console.debug($('#'+title+'_'+userId));
    $('#'+title+'_'+userId).css({visibility:'visible'});
}
function hideEdit(title,userId) {
    console.debug($('#'+title+'_'+userId));
    $('#'+title+'_'+userId).css({visibility:'hidden'});
}

//点击修改显示表单
function showForm(title,userId){
    console.debug($('#'+title+'_div_'+userId));
    $('#'+title+'_div_'+userId).css({display: 'inline'});
    $('#'+title+'_p_'+userId).css({display: 'none'});
}



function hideForm(title,userId){
    console.debug($('#'+title+'_div_'+userId));
    $('#'+title+'_div_'+userId).css({display: 'none'});
    $('#'+title+'_p_'+userId).css({display: 'flex'});
}

  // toastr.info('我们已向您的邮箱发送验证链接，请在点击确认后前往邮箱完成修改');