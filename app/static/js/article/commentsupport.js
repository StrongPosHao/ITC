function commentsupport(title,commentId,userId){
    //console.debug($('#comment_'+commentId+' a')[1]);
    if(title == '点赞'){
        console.debug($('#comment_'+commentId+' a[title="点赞"] span')[0]);
        console.debug($('#comment_'+commentId+' a[title="点赞"] span')[1]);
        console.debug($('#comment_'+commentId+' a[title="点赞"] span').css('color'));
        if($('#comment_'+commentId+' a[title="点赞"] span').css('color') != 'rgb(255, 165, 0)'){
            $('#comment_'+commentId+' a[title="点赞"] span').css({ color: 'orange' });
            supportpoint = parseInt($($('#comment_'+commentId+' a[title="点赞"] span')[1]).text());
            $($('#comment_'+commentId+' a[title="点赞"] span')[1]).text(supportpoint+1);

            toastr.success('点赞成功!');

            //设置踩不能被点击
            $('#comment_'+commentId+' a[title="没帮助"]').attr('href',"javascript:return false;");
            sendComment(title, commentId, userId,true)
        }else{
            $('#comment_'+commentId+' a[title="点赞"] span').css({ color: 'black' });
            supportpoint = parseInt($($('#comment_'+commentId+' a[title="点赞"] span')[1]).text());
            $($('#comment_'+commentId+' a[title="点赞"] span')[1]).text(supportpoint-1);

            toastr.info('取消点赞!');
            
            $('#comment_'+commentId+' a[title="没帮助"]').attr('href',"javascript:commentsupport('没帮助',"+commentId+")");
            sendComment(title, commentId, userId,false)
        }
    }
    if(title == '没帮助'){
        console.debug($('#comment_'+commentId+' a[title="没帮助"] span')[0]);
        console.debug($('#comment_'+commentId+' a[title="没帮助"] span')[1]);
        console.debug($('#comment_'+commentId+' a[title="没帮助"] span').css('color'));
        if($('#comment_'+commentId+' a[title="没帮助"] span').css('color') != 'rgb(255, 165, 0)'){
            $('#comment_'+commentId+' a[title="没帮助"] span').css({ color: 'orange' });
            supportpoint = parseInt($($('#comment_'+commentId+' a[title="没帮助"] span')[1]).text());
            $($('#comment_'+commentId+' a[title="没帮助"] span')[1]).text(supportpoint+1);

            toastr.success('踩成功!');

            //设置点赞不能被点击
            $('#comment_'+commentId+' a[title="点赞"]').attr('href',"javascript:return false;");
            sendComment(title, commentId, userId,true)
        }else{
            $('#comment_'+commentId+' a[title="没帮助"] span').css({ color: 'black' });
            supportpoint = parseInt($($('#comment_'+commentId+' a[title="没帮助"] span')[1]).text());
            $($('#comment_'+commentId+' a[title="没帮助"] span')[1]).text(supportpoint-1);

            toastr.info('取消踩!');

            $('#comment_'+commentId+' a[title="点赞"]').attr('href',"javascript:commentsupport('点赞',"+commentId+")");
            sendComment(title, commentId, userId,false)
        }
    }
}

//向后台发送Ajax请求
function sendComment(title, commentId, userId,ischecked) {
    $.ajax({
        url: '/SS',
        type: 'POST',
        data: 'title=' + title + '&commentId=' + commentId + '&userId=' + userId + '&ischecked=' + ischecked,
        success: function (data) {
        }
    });
}

function afterComment(parentId, articleId, userId) {
    // var content = $('#content_'+answerId).val();
    var content = $('#after_comment_' + parentId).val();
    $.ajax({
        url: '/question/after-comment',
        type: 'POST',
        data: 'parentId=' + parentId + '&articleId=' + articleId + '&content=' + content + '&userId=' + userId,
        success: function (data) {

        }
    });
}