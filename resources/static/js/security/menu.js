$(function () {
    // 格式化时间
    moment.locale(window.navigator.userLanguage || window.navigator.language);
    // 初始化父类菜单
    loadMenus();

    $("#exampleTableEvents").bootstrapTable({
        method: 'get',
        url: "/admin/security/menu/load",
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
            field: 'parent_code',
            title: 'Parent Code',
            sortable: true
        }, {
            field: 'menu_code',
            title: 'Menu Code',
            sortable: true
        }, {
            field: 'menu_name',
            title: 'Menu Name'
        }, {
            field: 'menu_url',
            title: 'Menu URL'
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
            width: 400,
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
                parent_code: $("#parent_code").val(),
                menu_code: $("#menu_code").val(),
                menu_name: $("#menu_name").val()
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
        layerModal("菜单 - 新增", ['783px', '500px'], "/admin/security/menu-add.html");
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
        menuDelete(ids);
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
    let menu_code = row["menu_code"];
    let result = "<div class='action-buttons'>" +
            "<a class='btn btn-primary btn-xs' href='javascript:void(0);' onclick='menuView(" + id + ");' title='View'><i class='fa fa-search-plus'></i> View</a>" +
            "<a class='btn btn-warning btn-xs' href='javascript:void(0);' onclick='menuEdit(" + id + ");' title='Edit'><i class='fa fa-pencil-square-o small'></i> Edit</a>" +
            "<a class='btn btn-warning btn-xs' href='javascript:void(0);' onclick='menuDelete(" + id + ");' title='Delete'><i class='fa fa-trash-o'></i> Delete</a>" +
            "<a class='btn btn-info btn-xs' href='javascript:void(0);' onclick='menuRoles(\"" + menu_code + "\");' title='Role'><i class='fa fa-address-card-o'></i> Role</a>" +
            "<a class='btn btn-info btn-xs' href='javascript:void(0);' onclick='menuUsers(\"" + menu_code + "\");' title='User'><i class='fa fa-user-o'></i> User</a>" +
        "</div>";
    return result;
}

/**
 * 菜单角色权限 视图
 *
 * @param menu_code 菜单编号
 */
function menuRoles(menu_code) {
    layerFullScreenModal("菜单角色权限 - [" + menu_code + "]", "/admin/security/menu-roles/" + menu_code + ".html");
}

/**
 * 菜单用户权限 视图
 *
 * @param menu_code 菜单编号
 */
function menuUsers(menu_code) {
    layerFullScreenModal("菜单用户权限 - [" + menu_code + "]", "/admin/security/menu-users/" + menu_code + ".html");
}

/**
 * 菜单视图
 *
 * @param id ID
 */
function menuView(id) {
    layerModal("菜单 - 查看", ['783px', '500px'], "/admin/security/menu-view/" + id + ".html");
}

/**
 * 菜单编辑
 *
 * @param id ID
 */
function menuEdit(id) {
    layerModal("菜单 - 编辑", ['783px', '500px'], "/admin/security/menu-edit/" + id + ".html");
}

/**
 * 菜单删除
 *
 * @param ids ID
 */
function menuDelete(ids) {
    layer.confirm('是否确定删除？', function(){
        ajaxRequest({
            type: "POST",
            url: "/admin/security/menu/delete",
            data: {"ids": ids},
            dataType: "json",
            isLoading: true,
            success: function (data) {
                layer.msg("删除成功行数: " + data._data, {icon: 1, time: 2000});
                // 刷新下拉列
                loadMenus();
                // 刷新列表
                $("#exampleTableEvents").bootstrapTable("refresh");
            },
            fail: function (data) {
                layer.msg(data._msg + ": " + data._data, {icon: 2, time: 3000});
            }
        });
    });
}

/**
 * 加载父类菜单
 */
function loadMenus() {
    ajaxRequest({
        type: "GET",
        url: "/admin/security/menu/list",
        data: {"parent_code": "0"},
        dataType: "json",
        isLoading: true,
        success: function (data) {
            $("#parent_code option:gt(1)").remove();
            $.each(data._data, function (idx, item) {
                $("#parent_code").append("<option value='" + item["menu_code"] + "'>" + item["menu_name"] + " [" + item["menu_code"] + "]</option>");
            });
            $("#parent_code" ).selectpicker("refresh");
        }
    });
}