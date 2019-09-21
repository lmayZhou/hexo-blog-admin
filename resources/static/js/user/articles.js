$(function () {
    // 格式化时间
    moment.locale(window.navigator.userLanguage || window.navigator.language);

    $("#exampleTableEvents").bootstrapTable({
        method: 'get',
        url: "/admin/articles/load",
        toolbar: '#exampleTableEventsToolbar', //工具按钮用哪个容器
        cache: false, // 设置为 false 禁用 AJAX 数据缓存， 默认为true
        striped: true, //表格显示条纹，默认为false
        pagination: true, // 在表格底部显示分页组件，默认false
        onlyInfoPagination: false,
        sortable: true, //是否启用排序
        sortName: "_id",
        sortOrder: 'desc', // 排序规则
        pageList: [10, 25, 50, 100, 500], // 设置页面可以显示的数据条数
        pageSize: 10, // 页面数据条数
        pageNumber: 1, // 首页页码
        sidePagination: 'server', // 分页方式：client客户端分页，server服务端分页（*）
        search: true, //是否显示表格搜索，此搜索是客户端搜索，不会进服务端
        strictSearch: true,
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
            field: '_id',
            title: 'ID',
            sortable: true
        }, {
            field: '_title',
            title: 'Title'
        }, {
            field: '_date',
            title: 'Date',
            sortable: true,
            formatter: function (value, row, index) {
                return moment.utc(value).format("YYYY-MM-DD HH:mm:ss");
            }
        }, {
            field: '_categories',
            title: 'Categories'
        }, {
            field: '_author',
            title: 'Author'
        }, {
            field: '_tags',
            title: 'Tags'
        }, {
            field:'',
            title: 'Operate',
            width: 150,
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
                author: author
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
        window.location.href = "/admin/article/add.html"
    });

    // 删除
    $("#del").click(function() {
        var selects = $("#exampleTableEvents").bootstrapTable("getSelections");
        var len = selects.length;
        if(!selects || len <= 0) {
            layer.msg("请至少选择一条数据！", {icon: 5});
            return;
        }
        var file_names = "";
        $.each(selects, function(i, item) {
            file_names += item._id;
            if((len - 1) != i) {
                file_names += ",";
            }
        });
        deleteArticle(file_names);
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
    var file_name = row["_file_name"];
    var result = "<div class='action-buttons'>" +
        "<a href='/admin/article/view/" + file_name + ".html' title='View'><span class='blue'><i class='fa fa-search-plus bigger-130'></i></span></a>" +
        "<a href='/admin/article/edit/" + file_name + ".html' title='Edit'><span class='green'><i class='fa fa-pencil-square-o bigger-130'></i></span></a>" +
        "<a href='javascript:deleteArticle(" + file_name + ");' title='Delete'><span class='red'><i class='fa fa-trash-o bigger-130'></i></span></a></div>";
    return result;
}

/**
 * 删除文章
 *
 * @param file_names 文章ID
 */
function deleteArticle(file_names) {
    layer.confirm('是否确定删除？', function(){
        ajaxRequest({
            type: "POST",
            url: "/admin/article/delete",
            data: {"file_names": file_names},
            dataType: "json",
            isLoading: true,
            success: function (data) {
                layer.msg("删除成功行数: " + data._data, {icon: 1, time: 2000});
                $("#exampleTableEvents").bootstrapTable("refresh");
            }
        });
    });
}