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
    // 格式化时间
    moment.locale(window.navigator.userLanguage || window.navigator.language);

    // 禁用编辑
    if("view" == operation) {
        $("form").find("input, select, textarea").attr("disabled", "disabled");
        $("form").find("button").hide();
    }

    // Form表单域重置
    $("#btn-reset").on("click", function () {
        $("#role_code").val("");
        $("#role_name").val("");
        $("#describe").val("");
    });

    // validate the comment form when it is submitted
    var formValidate = $("#commentForm").validate({
        submitHandler: function() {
            if("add" == operation) {
                ajaxRequest({
                    type: "POST",
                    url: "/admin/security/role/add",
                    data: {
                        "role_code": $("#role_code").val(),
                        "role_name": $("#role_name").val(),
                        "describe": $("#describe").val()
                    },
                    dataType: "json",
                    isLoading: true,
                    success: function (data) {
                        layer.msg(data._msg, {icon: 1, time: 2000}, function () {
                            // 父界面重新加载
                            window.parent.location.reload();
                            // 关闭窗口
                            // let index = parent.layer.getFrameIndex(window.name);
                            // parent.layer.close(index);
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
            } else if ("edit" == operation) {
                ajaxRequest({
                    type: "POST",
                    url: "/admin/security/role/edit",
                    data: {
                        "id": $("#id").val(),
                        "role_code": $("#role_code").val(),
                        "role_name": $("#role_name").val(),
                        "describe": $("#describe").val()
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
            }
        },
    });
});