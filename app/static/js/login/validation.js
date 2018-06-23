$(function () {
    //表单验证
    if ($(".login-form").size() > 0) {
        $(".login-form").validate({
            //校验规则
            rules: {
                username: {
                    required: true,
                    minlength: 2
                },
                password: {
                    required: true,
                    minlength: 7
                }

            },
            //校验的错误提示信息，应与校验规则一一对应
            messages: {
                username: {
                    required: "亲爱的用户:用户名不能为空!",
                    minlength: "亲爱的用户:用户名长度至少2位!"
                },
                password: {
                    required: "亲爱的用户:密码不能为空!",
                    minlength: jQuery.format("亲爱的用户:密码不能小于{0}个字符!")
                }
            }
        });
    }
    //后台验证

    if ($("#username").val() != null) {
        $("#username").blur(function () {
            console.debug($("#username").val());
            var username = $("#username").val();
            $.ajax({
                url: '/XX',
                type: 'POST',
                data: 'username=' + username,
                success: function (data) {
                    console.debug(data);
					$('#back-error1').text(data);
                }
            });
        });
    }
    if ($("#username").val() != null && $("#password").val() != null) {
        $("#password").blur(function () {
            console.debug($("#password").val());
            var username = $("#username").val();
            var password = $("#password").val();
            $.ajax({
                url: '/XX',
                type: 'POST',
                data: 'username=' + username + '&password=' + password,
                success: function (data) {
                    console.debug(data);
					$('#back-error2').text(data);
                }
            });
        });
    }
});
