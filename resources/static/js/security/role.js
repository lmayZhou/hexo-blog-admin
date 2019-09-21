$(function () {
    // 格式化时间
    moment.locale(window.navigator.userLanguage || window.navigator.language);

    $("#exampleTableEvents").bootstrapTable({
        method: 'get',
        url: "/admin/security/role/load",
        toolbar: '#exampleTableEventsToolbar', //工具按钮用哪个容器
        // toolbarAlign: 'right',
        cache: false, // 设置为 false 禁用 AJAX 数据缓存， 默认为true
        striped: true, //表格显示条纹，默认为false
        pagination: true, // 在表格底部显示分页组件，默认false
        onlyInfoPagination: false,
        sortable: true, //是否启用排序
        sortName: "id",
        sortOrder: 'asc', // 排序规则
        pageList: [10, 25, 50, 100, 500], // 设置页面可以显示的数据条数
        pageSize: 10, // 页面数据条数
        pageNumber: 1, // 首页页码
        sidePagination: 'server', // 分页方式：client客户端分页，server服务端分页（*）
        search: false, //是否显示表格搜索
        strictSearch: false,
        showToggle: true, //是否显示详细视图和列表视图的切换按钮
        showColumns: true, //是否显示所有的列
        showRefresh: true, //是否显示刷新按钮
        uniqueId: "id", //每一行的唯一标识，一般为主键列
        locale: window.navigator.userLanguage || window.navigator.language, //国际化
        iconSize: 'outline',
        icons: {
            refresh: 'glyphicon-repeat',
            toggle: 'glyphicon-list-alt',
            columns: 'glyphicon-list'
        },
        columns: [{
            checkbox: true,
            align: 'center'
        }, {
            field: 'id',
            title: 'ID',
            sortable: true
        }, {
            field: 'role_code',
            title: 'Role Code',
            sortable: true
        }, {
            field: 'role_name',
            title: 'Role Name'
        }, {
            field: 'describe',
            title: 'Describe'
        }, {
            field: 'last_date',
            title: 'Last Date',
            sortable: true,
            formatter: function (value, row, index) {
                return moment.utc(value).format("YYYY-MM-DD HH:mm:ss");
            }
        }, {
            field:'',
            title: 'Operate',
            width: 460,
            align: 'center',
            valign: 'middle',
            formatter: actionFormatter
        }],
        onLoadSuccess: function (data) {
            // 加载成功
        },
        onLoadError: function () {
            layer.msg("数据加载失败！", {icon: 5});
        },
        queryParams: function (params) {
            // 请求参数
            return {
                pageNumber: (params.offset / params.limit) + 1,
                pageSize: params.limit,
                sortName: params.sort,
                sortOrder: params.order,
                role_code: $("#role_code").val(),
                role_name: $("#role_name").val()
            };
        },
        responseHandler: function(rs) {
            // 响应参数
            return {
                "total": rs._data._total,
                "rows": rs._data._rows
            };
        }
    });

    // 新增
    $("#add").click(function() {
        layerModal("角色 - 新增", ['783px', '500px'], "/admin/security/role-add.html");
    });

    // 删除
    $("#del").click(function() {
        let selects = $("#exampleTableEvents").bootstrapTable("getSelections");
        const len = selects.length;
        if(!selects || len <= 0) {
            layer.msg("请至少选择一条数据！", {icon: 5});
            return;
        }
        let ids = "";
        $.each(selects, function(i, item) {
            ids += item.id;
            if((len - 1) != i) {
                ids += ",";
            }
        });
        roleDelete(ids);
    });

    // 搜索
    $("#search").click(function () {
        $("#exampleTableEvents").bootstrapTable("refresh");
    });
});

/**
 * 操作栏格式化
 *
 * @param {Object} value
 * @param {Object} row
 * @param {Object} index
 */
function actionFormatter(value, row, index) {
    let id = row["id"];
    let role_code = row["role_code"];
    let result = "<div class='action-buttons'>" +
            "<a class='btn btn-primary btn-xs' href='javascript:void(0);' onclick='roleView(" + id + ");' title='View'><i class='fa fa-search-plus'></i> View</a>" +
            "<a class='btn btn-warning btn-xs' href='javascript:void(0);' onclick='roleEdit(" + id + ");' title='Edit'><i class='fa fa-pencil-square-o small'></i> Edit</a>" +
            "<a class='btn btn-warning btn-xs' href='javascript:void(0);' onclick='roleDelete(" + id + ");' title='Delete'><i class='fa fa-trash-o'></i> Delete</a>" +
            "<a class='btn btn-info btn-xs' href='javascript:void(0);' onclick='roleMenus(\"" + role_code + "\");' title='Menu'><i class='fa fa-address-card-o'></i> Menu</a>" +
            "<a class='btn btn-info btn-xs' href='javascript:void(0);' onclick='roleResources(\"" + role_code + "\");' title='Resource'><i class='fa fa-address-card-o'></i> Resource</a>" +
            "<a class='btn btn-info btn-xs' href='javascript:void(0);' onclick='roleUsers(\"" + role_code + "\");' title='User'><i class='fa fa-user-o'></i> User</a>" +
        "</div>";
    return result;
}

/**
 * 角色菜单权限 视图
 *
 * @param role_code 角色编号
 */
function roleMenus(role_code) {
    layerFullScreenModal("角色菜单权限 - [" + role_code + "]", "/admin/security/role-menus/" + role_code + ".html");
}

/**
 * 角色资源权限 视图
 *
 * @param role_code 角色编号
 */
function roleResources(role_code) {
    layerFullScreenModal("角色资源权限 - [" + role_code + "]", "/admin/security/role-resources/" + role_code + ".html");
}

/**
 * 角色用户权限 视图
 *
 * @param role_code 角色编号
 */
function roleUsers(role_code) {
    layerFullScreenModal("角色用户权限 - [" + role_code + "]", "/admin/security/role-users/" + role_code + ".html");
}

/**
 * 角色视图
 *
 * @param id ID
 */
function roleView(id) {
    layerModal("角色 - 查看", ['783px', '360px'], "/admin/security/role-view/" + id + ".html");
}

/**
 * 角色编辑
 *
 * @param id ID
 */
function roleEdit(id) {
    layerModal("角色 - 编辑", ['783px', '400px'], "/admin/security/role-edit/" + id + ".html");
}

/**
 * 角色删除
 *
 * @param ids ID
 */
function roleDelete(ids) {
    layer.confirm('是否确定删除？', function(){
        ajaxRequest({
            type: "POST",
            url: "/admin/security/role/delete",
            data: {"ids": ids},
            dataType: "json",
            isLoading: true,
            success: function (data) {
                layer.msg("删除成功行数: " + data._data, {icon: 1, time: 2000});
                // 刷新列表
                $("#exampleTableEvents").bootstrapTable("refresh");
            },
            fail: function (data) {
                layer.msg(data._msg + ": " + data._data, {icon: 2, time: 3000});
            }
        });
    });
}