$(function () {
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green',
    });

    // 加载树形结构
    loadMenuTree("#resourceTree", zNodes);

    // 是否全部选中
    if(getCheckedNodes("resourceTree").length == zNodes.length) {
        $("input[name='checked-all']").iCheck("check");
    }

    // 全选/反选
    $("input[name='checked-all']").on("ifChanged", function() {
        checkAllNodes("resourceTree", $(this).is(':checked'));
    });

    // 提交
    $("#submit").on("click", function () {
        let nodes = getCheckedNodes("resourceTree");
        let resourceCodes = [];
        for(let i = 0; i < nodes.length; ++i) {
            resourceCodes.push(nodes[i].id);
        }
        ajaxRequest({
            type: "POST",
            url: "/admin/security/role/resources/save",
            data: {
                "role_code": role_code,
                "resource_codes": resourceCodes
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