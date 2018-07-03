var comment_id;
var answer_id;

function delete_comment(commentId) {
    comment_id = commentId;
    var info = "确定要删除该评论吗?";
    $('.modal.fade .modal-body').text(info);
}

function true_delete_comment() {
    if (comment_id) {
        sendDeleteComment(comment_id);
        toastr.success('删除成功!')
    }
}

function sendDeleteComment(comment_id) {
    $.ajax({
        url: '/question/delete-comment',
        type: 'POST',
        data: 'comment_id=' + comment_id,
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
        data: 'answer_id=' + answer_id,
        success: function (data) {
            window.location.reload();
        }
    })
}



