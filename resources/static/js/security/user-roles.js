$(function () {
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green',
    });

    // rol复选框选中
    for(let i = 0; i < user_roles.length; ++i) {
        $("input[type='checkbox'][value='" + user_roles[i].role_code + "']").iCheck("check");
    }

    // 是否全部选中
    if(isCheck("#rolesList")) {
        $("input[name='checked-all']").iCheck("check");
    }

    // 全选/反选
    $("input[name='checked-all']").on("ifChanged", function() {
        if($(this).is(":checked")) {
            $("#rolesList :checkbox").iCheck("check");
            return;
        }
        $("#rolesList :checkbox").iCheck("uncheck");
    });

    // 提交
    $("#submit").on("click", function () {
        let roleCodes = checkVal("#rolesList");
        ajaxRequest({
            type: "POST",
            url: "/admin/security/user/roles/save",
            data: {
                "user_id": user_id,
                "role_codes": roleCodes
            },
            dataType: "json",
            isLoading: true,
            success: function (data) {
                layer.msg(data._msg, {icon: 1, time: 2000}, function () {
                    // 关闭窗口
                    let index = parent.layer.getFrameIndex(window.name);
                    parent.layer.close(index);
                });
            }
        });
    });
});