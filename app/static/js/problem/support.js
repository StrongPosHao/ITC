function commentsupport(title, commentId, userId) {
    //console.debug($('#comment_'+commentId+' a')[1]);
    if (title == '点赞') {
        console.debug($('#comment_' + commentId + ' a[title="点赞"] span')[0]);
        console.debug($('#comment_' + commentId + ' a[title="点赞"] span')[1]);
        console.debug($('#comment_' + commentId + ' a[title="点赞"] span').css('color'));
        if ($('#comment_' + commentId + ' a[title="点赞"] span').css('color') != 'rgb(255, 165, 0)') {
            $('#comment_' + commentId + ' a[title="点赞"] span').css({color: 'orange'});
            supportpoint = parseInt($($('#comment_' + commentId + ' a[title="点赞"] span')[1]).text());
            $($('#comment_' + commentId + ' a[title="点赞"] span')[1]).text(supportpoint + 1);

            //设置踩不能被点击
            $('#comment_' + commentId + ' a[title="没帮助"]').attr('href', "javascript:return false;");
            toastr.success('点赞成功!');
            sendSupport(title, commentId, userId, true)
        } else {
            $('#comment_' + commentId + ' a[title="点赞"] span').css({color: 'black'});
            supportpoint = parseInt($($('#comment_' + commentId + ' a[title="点赞"] span')[1]).text());
            $($('#comment_' + commentId + ' a[title="点赞"] span')[1]).text(supportpoint - 1);

            $('#comment_' + commentId + ' a[title="没帮助"]').attr('href', "javascript:commentsupport('没帮助'," + commentId + ")");
            toastr.info('取消点赞!');
            sendSupport(title, commentId, userId, false)
        }
    }
    if (title == '没帮助') {
        console.debug($('#comment_' + commentId + ' a[title="没帮助"] span')[0]);
        console.debug($('#comment_' + commentId + ' a[title="没帮助"] span')[1]);
        console.debug($('#comment_' + commentId + ' a[title="没帮助"] span').css('color'));
        if ($('#comment_' + commentId + ' a[title="没帮助"] span').css('color') != 'rgb(255, 165, 0)') {
            $('#comment_' + commentId + ' a[title="没帮助"] span').css({color: 'orange'});
            supportpoint = parseInt($($('#comment_' + commentId + ' a[title="没帮助"] span')[1]).text());
            $($('#comment_' + commentId + ' a[title="没帮助"] span')[1]).text(supportpoint + 1);

            //设置点赞不能被点击
            $('#comment_' + commentId + ' a[title="点赞"]').attr('href', "javascript:return false;");
            toastr.success('踩成功!');
            sendSupport(title, commentId, userId, true)
        } else {
            $('#comment_' + commentId + ' a[title="没帮助"] span').css({color: 'black'});
            supportpoint = parseInt($($('#comment_' + commentId + ' a[title="没帮助"] span')[1]).text());
            $($('#comment_' + commentId + ' a[title="没帮助"] span')[1]).text(supportpoint - 1);

            $('#comment_' + commentId + ' a[title="点赞"]').attr('href', "javascript:commentsupport('点赞'," + commentId + ")");
            toastr.info('取消踩!');
            sendSupport(title, commentId, userId, false)
        }
    }
}

//向后台发送Ajax请求
function sendSupport(title, answerId, userId, ischecked) {
    if (title === '点赞') {
        $.ajax({
            url: '/question/like-answer',
            type: 'POST',
            data: 'title=' + title + '&answerId=' + answerId + '&userId=' + userId + '&ischecked=' + ischecked,
            success: function (data) {
            }
        });
    } else if (title === '没帮助') {
        $.ajax({
            url: '/question/unlike-answer',
            type: 'POST',
            data: 'title=' + title + '&answerId=' + answerId + '&userId=' + userId + '&ischecked=' + ischecked,
            success: function (data) {
            }
        });
    }

}