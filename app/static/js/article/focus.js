//关注作者
function focus(user_id,writer_id){
  console.debug($('.plus').text())
  if($('.plus').text()=='关注'){
    $('.plus').html('<span style="color:blue"><span class="glyphicon glyphicon-plus"></span>已关注</span>')
    send_to_back(user_id,writer_id,true);
  }else{
    $('.plus').html('<span><span class="glyphicon glyphicon-plus"></span>关注</span>')
    send_to_back(user_id,writer_id,false);
  }
}
//向后台发送Ajax请求
function send_to_back(user_id,writer_id,ischecked) {
    $.ajax({
        url: '/XX',
        type: 'POST',
        data: 'user_id=' + user_id + '&writer_id=' + writer_id + '&ischecked' + ischecked,
        success: function (data) {
        }
    });
}