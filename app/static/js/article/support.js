//点赞,踩，举报等的样式变化
function support(title, user_id, article_id) {
    if (title != '评论') {
        //如果第一次是点赞rgb(230, 126, 34)
        console.debug($(".btn.support[title=" + title + "] span").css('color'));
        if ($(".btn.support[title=" + title + "] span").css('color') != 'rgb(255, 163, 33)') {
            console.debug(title);
            console.debug($(".btn.support[title=" + title + "] span"));
            $(".btn.support[title=" + title + "] span").css({ color: '#ffa321' });
            console.debug($(".btn.support[title=" + title + "] span").css('color') == 'rgb(255, 163, 33)');
            support_point = $(".btn.support[title=" + title + "] .support-num span").text()
            console.debug($(".btn.support[title=" + title + "] .support-num span").text(parseInt(support_point) + 1));

            //如果当前是点赞，就不能踩和举报
            if (title == '点赞') {
                $(".btn.support[title='没帮助']").attr('disabled', true);
                $(".btn.support[title='举报']").attr('disabled', true);
            }
            if (title == '没帮助' || title == '举报') {
                $(".btn.support[title='点赞']").attr('disabled', true);
            }
            //向后台发送数据
            send_to_back(title, user_id, article_id, true);
        } else {
            console.debug(title);
            console.debug($(".btn.support[title=" + title + "] span"));
            $(".btn.support[title=" + title + "] span").css({ color: 'black' });
            console.debug($(".btn.support[title=" + title + "] span").css('color') == 'black');
            support_point = $(".btn.support[title=" + title + "] .support-num span").text()
            console.debug($(".btn.support[title=" + title + "] .support-num span").text(parseInt(support_point) - 1));

            //如果当前是取消点赞，就能踩和举报
            if (title == '点赞') {
                $(".btn.support[title='没帮助']").attr('disabled', false);
                $(".btn.support[title='举报']").attr('disabled', false);
            }
            if ($(".btn.support[title='没帮助'] span").css('color') != 'rgb(255, 163, 33)' && ($(".btn.support[title='举报'] span").css('color') != 'rgb(255, 163, 33)')) {
                $(".btn.support[title='点赞']").attr('disabled', false);
            }
            if ($(".btn.support[title='举报'] span").css('color') != 'rgb(255, 163, 33)' && ($(".btn.support[title='没帮助'] span").css('color') != 'rgb(255, 163, 33)')) {
                $(".btn.support[title='点赞']").attr('disabled', false);
            }
            //向后台发送数据
            send_to_back(title, user_id, article_id, false);
        }
        console.debug('踩' + $(".btn.support[title='没帮助'] span").css('color'));
        console.debug('举报' + $(".btn.support[title='举报'] span").css('color'));
    }
}

//向后台发送Ajax请求
function send_to_back(title, user_id, article_id, ischecked) {
    $.ajax({
        url: '/XX',
        type: 'POST',
        data: 'title=' + title + '&user_id=' + user_id + '&article_id=' + article_id + '&ischecked' + ischecked,
        success: function (data) {
        }
    });
}