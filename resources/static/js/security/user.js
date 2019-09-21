$(function () {
    // 格式化时间
    moment.locale(window.navigator.userLanguage || window.navigator.language);

    $("#exampleTableEvents").bootstrapTable({
        method: 'get',
        url: "/admin/security/user/load",
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
            field: 'nickname',
            title: 'Nickname'
        }, {
            field: 'email',
            title: 'Email'
        }, {
            field: 'sex',
            title: 'Sex',
            align: 'center',
            formatter: function (value) {
                let label = "<span class='badge badge-warning'>未知</span>";
                if(1 == value) {
                    label = "<span class='badge badge-info'>男</span>";
                } else if(2 == value) {
                    label = "<span class='badge badge-danger'>女</span>";
                }
                return label;
            }
        }, {
            field: 'qq',
            title: 'QQ'
        }, {
            field: 'icon',
            title: 'Icon'
        }, {
            field: 'is_available',
            title: 'Is Available',
            align: 'center',
            formatter: function (value) {
                let label = "<span class='badge badge-warning'>禁用</span>";
                if(1 == value) {
                    label = "<span class='badge badge-primary'>启用</span>";
                }
                return label;
            }
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
            width: 480,
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
                id: $("#user_id").val(),
                sex: $("#sex").val(),
                user_name: $("#user_name").val()
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
        layerModal("用户 - 新增", ['783px', '500px'], "/admin/security/user-add.html");
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
        userDelete(ids);
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
    let is_available = row["is_available"];
    let result = "<div class='action-buttons'>";
    let is_available_a = "<a class='btn btn-warning btn-xs' href='javascript:void(0);' onclick='isDisable(" + id + ");' title='Disable'><i class='fa fa-lock'></i> Disable</a>";
    if(0 == is_available) {
        is_available_a = "<a class='btn btn-info btn-xs' href='javascript:void(0);' onclick='isEnable(" + id + ");' title='Enable'><i class='fa fa-unlock'></i> Enable</a>";
    }
    result += "<a class='btn btn-primary btn-xs' href='javascript:void(0);' onclick='userView(" + id + ");' title='View'><i class='fa fa-search-plus'></i> View</a>" +
            "<a class='btn btn-warning btn-xs' href='javascript:void(0);' onclick='userEdit(" + id + ");' title='Edit'><i class='fa fa-pencil-square-o small'></i> Edit</a>" +
            "<a class='btn btn-warning btn-xs' href='javascript:void(0);' onclick='userDelete(" + id + ");' title='Delete'><i class='fa fa-trash-o'></i> Delete</a>" +
            is_available_a +
            "<a class='btn btn-info btn-xs' href='javascript:void(0);' onclick='userMenus(\"" + id + "\");' title='Menu'><i class='fa fa-address-card-o'></i> Menu</a>" +
            "<a class='btn btn-info btn-xs' href='javascript:void(0);' onclick='userResources(\"" + id + "\");' title='Resource'><i class='fa fa-address-card-o'></i> Resource</a>" +
            "<a class='btn btn-info btn-xs' href='javascript:void(0);' onclick='userRoles(\"" + id + "\");' title='Role'><i class='fa fa-user-o'></i> Role</a>" +
        "</div>";
    return result;
}

/**
 * 用户菜单权限 视图
 *
 * @param id 用户编号
 */
function userMenus(id) {
    layerFullScreenModal("用户菜单权限 - [" + id + "]", "/admin/security/user-menus/" + id + ".html");
}

/**
 * 用户资源权限 视图
 *
 * @param id 用户编号
 */
function userResources(id) {
    layerFullScreenModal("用户资源权限 - [" + id + "]", "/admin/security/user-resources/" + id + ".html");
}

/**
 * 用户角色权限 视图
 *
 * @param id 用户编号
 */
function userRoles(id) {
    layerFullScreenModal("用户角色权限 - [" + id + "]", "/admin/security/user-roles/" + id + ".html");
}

/**
 * 用户视图
 *
 * @param id ID
 */
function userView(id) {
    layerModal("用户 - 查看", ['783px', '500px'], "/admin/security/user-view/" + id + ".html");
}

/**
 * 用户编辑
 *
 * @param id ID
 */
function userEdit(id) {
    layerModal("用户 - 编辑", ['783px', '500px'], "/admin/security/user-edit/" + id + ".html");
}

/**
 * 用户删除
 *
 * @param ids ID
 */
function userDelete(ids) {
    layer.confirm('是否确定删除？', function(){
        ajaxRequest({
            type: "POST",
            url: "/admin/security/user/delete",
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

/**
 * 禁用
 *
 * @param id
 */
function isDisable(id) {
    ajaxRequest({
        type: "POST",
        url: "/admin/security/user/is_disable",
        data: {"id": id, "is_available": 0},
        dataType: "json",
        isLoading: true,
        success: function (data) {
            // 刷新列表
            $("#exampleTableEvents").bootstrapTable("refresh");
        },
        fail: function (data) {
            layer.msg(data._msg + ": " + data._data, {icon: 2, time: 3000});
        }
    });
}

/**
 * 启用
 *
 * @param id
 */
function isEnable(id) {
    ajaxRequest({
        type: "POST",
        url: "/admin/security/user/is_disable",
        data: {"id": id, "is_available": 1},
        dataType: "json",
        isLoading: true,
        success: function (data) {
            // 刷新列表
            $("#exampleTableEvents").bootstrapTable("refresh");
        },
        fail: function (data) {
            layer.msg(data._msg + ": " + data._data, {icon: 2, time: 3000});
        }
    });
}