$(function () {
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green',
    });

    // 加载树形结构
    loadMenuTree("#menuTree", zNodes);

    // 是否全部选中
    if(getCheckedNodes("menuTree").length == zNodes.length) {
        $("input[name='checked-all']").iCheck("check");
    }

    // 全选/反选
    $("input[name='checked-all']").on("ifChanged", function() {
        checkAllNodes("menuTree", $(this).is(':checked'));
    });

    // 提交
    $("#submit").on("click", function () {
        let nodes = getCheckedNodes("menuTree");
        let menuCodes = [];
        for(let i = 0; i < nodes.length; ++i) {
            menuCodes.push(nodes[i].id);
        }
        ajaxRequest({
            type: "POST",
            url: "/admin/security/user/menus/save",
            data: {
                "user_id": user_id,
                "menu_codes": menuCodes
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