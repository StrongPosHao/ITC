$(function(){
    //在一开始就要向后台发送请求确定总共有多少页
    var url = window.location.href
    url1 = '/admin'+url.substring(url.lastIndexOf("/"))+'/changepage'
    url = '/admin'+url.substring(url.lastIndexOf("/"))+'/gettotalpage'
    //向后台发数据获取总页数
    send_to_back(url)

});

//向后台发送Ajax请求,删除单个
function send_to_back(url) {
    $.ajax({
        url: url,
        type: 'GET',
        data: '',
        success: function (data) {
            var data = eval("("+data+")")
            allPage1 = data.size
            //设置分页
            setPage(allPage1,6,1,1)
            //设置点击事件
            //末页
            $('.spLast').click(function(){
                send_to_back2(allPage1)
            });
            //首页
            $('.spFirst').click(function(){
                send_to_back2(1)
            });
            //中间的页面
            $.each($('.spCover li'),function(index,item){
                $(item).click(function(){
                    send_to_back2(parseInt($(item).first().text()))
                });
            });
            //上一页，下一页
            $('.spNext').click(function(){
                send_to_back2(-1)
            });
            //首页
            $('.spPrev').click(function(){
                send_to_back2(-2)
            });
        }
    });
}

//向后台发送数据改变页面
function send_to_back2(current) {
    $.ajax({
        url: url1,
        type: 'POST',
        data: 'current=' + current,
        success: function (data) {
           var data = eval("("+data+")")
           $('.table.table-hover.table-striped tbody').html("");


           for(var i = 0;i<data.length;i++){
                var content = "<tr>"+"<td><input type='checkbox' class='user'/></td>"
                var temp = "<td>"
                temp = temp+data[i].id
                temp = temp + "</td>"

                var temp1 = "<td>"
                temp1 = temp1+data[i].username
                temp1 = temp1 + "</td>"

                var temp2 = "<td>"
                temp2 = temp2+data[i].email
                temp2 = temp2 + "</td>"

                var temp3 = "<td>"
                temp3 = temp3+data[i].phone
                temp3 = temp3 + "</td>"

                var temp4 = "<td>"
                temp4 = temp4+data[i].permission
                temp4 = temp4 + "</td>"

                var temp5 = "<td><button class='btn btn-danger btn-sm' data-toggle='modal'data-target='#modal_del'onclick='singledelete("+data[i].id+",'"+data[i].username+"')'>删除</button></td>"
                console.debug(temp5)

                content = content+temp+temp1+temp2+temp3+temp4+temp5
                content  = content + "</tr>"
                $('.table.table-hover.table-striped tbody').append(content)
           }
           //局部刷新
           $(".table.table-hover.table-striped").load("http://127.0.0.1:5000/admin/user .table.table-hover.table-striped");
            //window.location.reload();
        }
    });
}

//设置分页
function setPage(allPage1,showPage1,startPage1,initPage1){
    $(".simplePaging2").simplePaging({
            allPage: allPage1,
            showPage: showPage1,
            startPage: startPage1,
            initPage: initPage1
     });
}