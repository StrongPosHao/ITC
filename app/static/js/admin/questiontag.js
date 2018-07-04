var qid
function listTag(questionId){
    console.debug(questionId)
    send_to_backs(questionId)
    send_to_backs1()
}
//向后台发送Ajax请求,获得已分配标签
function send_to_backs(questionId) {
    qid = questionId
    $.ajax({
        url: '/admin/questiontag',
        type: 'POST',
        data: 'questionId=' + questionId,
        success: function (data) {
            $('#select2').html("")
            //将获取的字符串变为json对象
            var json = eval("("+data+")")
            console.debug(json)
            for(var i=0,l=json.length;i<l;i++){
                console.debug(json[i].name)
                $('#select2').append("<option value="+json[i].tagId+">"+json[i].name+"</option>")
            }
        }
    });
}
//向后台发送Ajax请求,获得所有标签
function send_to_backs1(questionId) {
    $.ajax({
        url: '/admin/questiontag/all',
        type: 'POST',
        success: function (data) {
            $('#select1').html("")
            //将获取的字符串变为json对象
            var json = eval("("+data+")")
            console.debug(json)
            for(var i=0,l=json.length;i<l;i++){
                console.debug(json[i].name)
                $('#select1').append("<option value="+json[i].tagId+">"+json[i].name+"</option>")
            }

            //此处要解决已分配的标签不应出现在所有标签中
            //首先拿到所有已分配的value
            var ids = $.map($('#select2 option'),function(item){
                return item.value;
            });
            //现在ids就是已分配标签的id数组
            console.debug(ids)

            //遍历所有标签，判断id是否在数组中，如果在的话就移除
            $.each($('#select1 option'),function(index,item){
                if($.inArray(item.value,ids)>=0){
                    $(item).remove();
                }
            });

        }
    });
}

//点击确认之后，需要向后台发送请求，修改文章的标签
function confirmtag(){
    var tagIds = []
     $.each($('#select2 option'),function(index,item){
        console.log(item.value);
        tagIds.push(item.value);
     });
     send_to_backs3(tagIds)
     toastr.success("修改标签成功!")
}
//向后台发送Ajax请求,获得已分配标签
function send_to_backs3(tagIds) {
    $.ajax({
        url: '/admin/questiontag/changetag',
        type: 'POST',
        data: 'tagIds=' + tagIds + '&questionId=' + qid,
        success: function (data) {
            window.location.reload();
        }
    });
}