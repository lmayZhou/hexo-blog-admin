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

    // 加载父类菜单
    loadResources();

    // 禁用编辑
    if("view" == operation) {
        $("form").find("input, select, textarea").attr("disabled", "disabled");
        $("form").find("button").hide();
    }

    // 下拉赋值
    if(resource_level) {
        $("#resource_level").selectpicker("val", resource_level);
    }
    $("#resource_level" ).selectpicker("refresh");

    // Form表单域重置
    $("#btn-reset").on("click", function () {
        $("#parent_code").selectpicker("val", "0");
        $("#resource_level").selectpicker("val", "0");
        $("#resource_code").val("");
        $("#resource_name").val("");
        $("#resource_url").val("");
        $("#describe").val("");
    });

    // validate the comment form when it is submitted
    var formValidate = $("#commentForm").validate({
        submitHandler: function() {
            if("add" == operation) {
                ajaxRequest({
                    type: "POST",
                    url: "/admin/security/resource/add",
                    data: {
                        "parent_code": $("#parent_code").val(),
                        "resource_code": $("#resource_code").val(),
                        "resource_level": $("#resource_level").val(),
                        "resource_name": $("#resource_name").val(),
                        "resource_url": $("#resource_url").val(),
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
                    url: "/admin/security/resource/edit",
                    data: {
                        "id": $("#id").val(),
                        "parent_code": $("#parent_code").val(),
                        "resource_code": $("#resource_code").val(),
                        "resource_level": $("#resource_level").val(),
                        "resource_name": $("#resource_name").val(),
                        "resource_url": $("#resource_url").val(),
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

/**
 * 加载父类菜单
 */
function loadResources() {
    ajaxRequest({
        type: "GET",
        url: "/admin/security/resource/list",
        data: {"resource_level": [0, 1]},
        dataType: "json",
        isLoading: true,
        success: function (data) {
            $("#parent_code option:gt(0)").remove();
            $.each(data._data, function (idx, item) {
                let options = "<option value='" + item["resource_code"] + "'>";
                if(1 == item.resource_level) {
                    options += "&emsp;&emsp;├ ";
                }
                options += item["resource_name"] + " [" + item["resource_code"] + "]</option>";
                $("#parent_code").append(options);
            });
            // 下拉赋值
            if(parent_code) {
                $("#parent_code").selectpicker("val", parent_code);
            }
            $("#parent_code" ).selectpicker("refresh");
        }
    });
}