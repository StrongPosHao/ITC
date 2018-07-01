function post_answerId(answerId, questionId) {
    var content = $('#content_'+answerId).val();
    var data = {
        data: JSON.stringify({
            'content': content,
            'answerId': answerId,
            'questionId': questionId
        })
    };
    $.ajax({
        url: '/question/comment_answer',
        type: 'POST',
        data: data,
        success: function (res) {
            window.location.reload();
        },
    });
}

//点击评论他人，评论框显示出来
function saycomment(commentId){
    console.debug($('#comment_'+commentId+' + div .' + 'write-comment'));
    $('#comment_'+commentId+' + div .' + 'write-comment').css({ display:'inline' });
}