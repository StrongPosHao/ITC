var comment_id;
var answer_id;

function delete_comment(commentId) {
    comment_id = commentId;
    console.debug('The comment_id' + comment_id);
    var info = "确定要删除该评论吗?";
    $('.modal.fade .modal-body').text(info);
}

function sendDeleteComment() {
    $.ajax({
        url: '/question/delete-comment',
        type: 'POST',
        data: 'commentId=' + comment_id,
        success: function (data) {
            window.location.reload();
        }
    })
}

function delete_answer(answerId) {
    answer_id = answerId;
    var info = "确定要删除该回答吗?";
    $('.modal.fade .modal-body').text(info);
}

function true_delete() {
    if (answer_id) {
        sendDeleteAnswer();
    } else if (comment_id) {
        sendDeleteComment()
    }
    toastr.success('删除成功!');
}

function sendDeleteAnswer() {
    $.ajax({
        url: '/question/delete-answer',
        type: 'POST',
        data: 'answerId=' + answer_id,
        success: function (data) {
            window.location.reload();
        }
    })
}



