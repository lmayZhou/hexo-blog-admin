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

    if("edit" == operation) {
        $("#nickname").attr("disabled", "disabled");
    }

    // 下拉赋值
    if(sex) {
        $("#sex").selectpicker("val", sex);
    }
    $("#sex" ).selectpicker("refresh");

    // Form表单域重置
    $("#btn-reset").on("click", function () {
        $("#nickname").val("");
        $("#sex").selectpicker("val", "0");
        $("#email").val("");
        $("#qq").val("");
        $("#icon").val("");
    });

    // validate the comment form when it is submitted
    var formValidate = $("#commentForm").validate({
        submitHandler: function() {
            if("add" == operation) {
                ajaxRequest({
                    type: "POST",
                    url: "/admin/security/user/add",
                    data: {
                        "nickname": $("#nickname").val(),
                        "sex": $("#sex").val(),
                        "email": $("#email").val(),
                        "qq": $("#qq").val(),
                        "icon": $("#icon").val()
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
                    url: "/admin/security/user/edit",
                    data: {
                        "id": $("#id").val(),
                        "sex": $("#sex").val(),
                        "icon": $("#icon").val(),
                        // "nickname": $("#nickname").val(),
                        "email": $("#email").val(),
                        "qq": $("#qq").val()
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