/**
 * jQuery Validation插件兼容Bootstrap的方法
 */
$.validator.setDefaults({
    highlight: function (element) {
        $(element).closest('.form-group').removeClass('has-success').addClass('has-error');
    },
    success: function (element) {
        $(element).closest('.form-group').removeClass('has-error').addClass('has-success');
    },
    errorElement: "span",
    errorPlacement: function (error, element) {
        if (element.is(":radio") || element.is(":checkbox")) {
            error.appendTo($(element).parent().parent().parent());
        } else {
            error.appendTo($(element).parent());
        }
    },
    errorClass: "help-block m-b-none",
    validClass: "help-block m-b-none"
});

$(function () {
    // Form表单域重置
    $("#btn-reset").on("click", function () {
        $("#old_password").val("");
        $("#password").val("");
        $("#role_name").val("");
    });

    // validate the comment form when it is submitted
    var formValidate = $("#commentForm").validate({
        rules: {
            confirm_password: {
                equalTo: "#password"
            }
        },
        submitHandler: function() {
            ajaxRequest({
                type: "POST",
                url: "/admin/modify-password",
                data: {
                    "id": $("#id").val(),
                    "old_password": $("#old_password").val(),
                    "password": $("#password").val(),
                    "confirm_password": $("#confirm_password").val()
                },
                dataType: "json",
                isLoading: true,
                success: function (data) {
                    layer.msg(data._msg, {icon: 1, time: 2000}, function () {
                        // 父界面重新加载
                        window.parent.location.reload();
                    });
                },
                fail: function (data) {
                    if(-107 == data._code) {
                        // 后台校验失败反馈
                        formValidate.showErrors(data._data);
                        return;
                    }
                    layer.msg(data._msg + ": " + data._data, {icon: 5, time: 3000});
                }
            });
        },
    });
});