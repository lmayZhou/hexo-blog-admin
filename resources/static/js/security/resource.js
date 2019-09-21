$(function () {
    // 格式化时间
    moment.locale(window.navigator.userLanguage || window.navigator.language);
    // 初始化父类菜单
    loadResources();

    $("#exampleTableEvents").bootstrapTable({
        method: 'get',
        url: "/admin/security/resource/load",
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
            field: 'resource_code',
            title: 'Resource Code',
            sortable: true
        }, {
            field: 'resource_name',
            title: 'Resource Name'
        }, {
            field: 'resource_url',
            title: 'Resource URL'
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
                resource_code: $("#resource_code").val(),
                resource_name: $("#resource_name").val()
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
        layerModal("资源 - 新增", ['783px', '500px'], "/admin/security/resource-add.html");
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
        resourceDelete(ids);
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
    let resource_code = row["resource_code"];
    let result = "<div class='action-buttons'>" +
            "<a class='btn btn-primary btn-xs' href='javascript:void(0);' onclick='resourceView(" + id + ");' title='View'><i class='fa fa-search-plus'></i> View</a>" +
            "<a class='btn btn-warning btn-xs' href='javascript:void(0);' onclick='resourceEdit(" + id + ");' title='Edit'><i class='fa fa-pencil-square-o small'></i> Edit</a>" +
            "<a class='btn btn-warning btn-xs' href='javascript:void(0);' onclick='resourceDelete(" + id + ");' title='Delete'><i class='fa fa-trash-o'></i> Delete</a>" +
            "<a class='btn btn-info btn-xs' href='javascript:void(0);' onclick='resourceRoles(\"" + resource_code + "\");' title='Role'><i class='fa fa-address-card-o'></i> Role</a>" +
            "<a class='btn btn-info btn-xs' href='javascript:void(0);' onclick='resourceUsers(\"" + resource_code + "\");' title='User'><i class='fa fa-user-o'></i> User</a>" +
        "</div>";
    return result;
}

/**
 * 资源角色权限 视图
 *
 * @param resource_code 资源编号
 */
function resourceRoles(resource_code) {
    layerFullScreenModal("资源角色权限 - [" + resource_code + "]", "/admin/security/resource-roles/" + resource_code + ".html");
}

/**
 * 资源用户权限 视图
 *
 * @param resource_code 资源编号
 */
function resourceUsers(resource_code) {
    layerFullScreenModal("资源用户权限 - [" + resource_code + "]", "/admin/security/resource-users/" + resource_code + ".html");
}

/**
 * 资源视图
 *
 * @param id ID
 */
function resourceView(id) {
    layerModal("资源 - 查看", ['783px', '500px'], "/admin/security/resource-view/" + id + ".html");
}

/**
 * 资源编辑
 *
 * @param id ID
 */
function resourceEdit(id) {
    layerModal("资源 - 编辑", ['783px', '600px'], "/admin/security/resource-edit/" + id + ".html");
}

/**
 * 资源删除
 *
 * @param ids ID
 */
function resourceDelete(ids) {
    layer.confirm('是否确定删除？', function(){
        ajaxRequest({
            type: "POST",
            url: "/admin/security/resource/delete",
            data: {"ids": ids},
            dataType: "json",
            isLoading: true,
            success: function (data) {
                layer.msg("删除成功行数: " + data._data, {icon: 1, time: 2000});
                // 刷新下拉列
                loadResources();
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
function loadResources() {
    ajaxRequest({
        type: "GET",
        url: "/admin/security/resource/list",
        data: {"resource_level": [0, 1]},
        dataType: "json",
        isLoading: true,
        success: function (data) {
            $("#parent_code option:gt(1)").remove();
            $.each(data._data, function (idx, item) {
                let options = "<option value='" + item["resource_code"] + "'>";
                if(1 == item.resource_level) {
                    options += "&emsp;&emsp;├ ";
                }
                options += item["resource_name"] + " [" + item["resource_code"] + "]</option>";
                $("#parent_code").append(options);
            });
            $("#parent_code" ).selectpicker("refresh");
        }
    });
}