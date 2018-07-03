var comment_id;


function delete_comment(commentId) {
    comment_id = commentId;
    var info = "确定要删除该评论吗?";
    $('.modal.fade .modal-body').text(info)
}

function true_delete() {
    if (comment_id) {
        sendDelete(comment_id);
        toastr.success('删除成功!')
    }
}

function sendDelete(comment_id) {
    $.ajax({
        url: '/question/content/delete',
        type: 'POST',
        data: 'comment_id=' + comment_id,
        success: function (data) {
            window.location.reload();
        }
    })
}

