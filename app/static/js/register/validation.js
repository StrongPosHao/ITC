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
                email: {
                    required: true,
                    email: true
                },
                phone: {
                    required: true,
                    number: true,
                    rangelength: [11, 11]
                },
                password: {
                    required: true,
                    minlength: 7
                },
                confirm: {
                    required: true,
                    minlength: 7,
                    equalTo: "#password"
                }
            },
            //校验的错误提示信息，应与校验规则一一对应
            messages: {
                username: {
                    required: "亲爱的用户:用户名不能为空!",
                    minlength: "亲爱的用户:用户名长度至少2位!"
                },
                email: {
                    required: "亲爱的用户:Email地址不能为空!",
                    email: "亲爱的用户:请输入正确的email地址!"
                },
                phone: {
                    required: "亲爱的用户:手机号不能为空!",
                    number: "亲爱的用户:手机号必须为数字!",
                    rangelength: "亲爱的用户:请输入正确的手机位数!"
                },
                password: {
                    required: "亲爱的用户:密码不能为空!",
                    minlength: jQuery.format("亲爱的用户:密码不能小于{0}个字符!")
                },
                confirm: {
                    required: "亲爱的用户:确认密码不能为空!",
                    minlength: "亲爱的用户:确认密码不能小于7个字符!",
                    equalTo: "亲爱的用户:两次输入密码不一致!"
                }
            }
        });
    }
});