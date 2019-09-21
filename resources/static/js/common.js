/**
 * Ajax 请求
 *
 * @param param 请求参数
 */
function ajaxRequest(param) {
    if (!param.contentType) {
        param.contentType = "application/x-www-form-urlencoded; charset=UTF-8";
    }
    if (!param.type) {
        param.type = "GET";
    }
    if (!param.async) {
        param.async = true;
    }
    if (!param.dataType) {
        param.dataType = "json";
    }

    var index = 0;
    $.ajax({
        url: param.url,
        type: param.type,
        async: param.async,
        data: param.data,
        timeout: 0,
        dataType: param.dataType,
        contentType: param.contentType,
        headers: {"X-CSRFToken": $("#csrf_token").val()},
        beforeSend: function (xhr) {
            if (param.isLoading) {
                index = layer.load(1);
            }
            if (typeof param.beforeSend == "function") {
                param.beforeSend();
            }
        },
        success: function (data) {
            if (200 == data._code) {
                if (typeof param.success == "function") {
                    param.success(data);
                }
            } else {
                if (typeof param.fail == "function") {
                    param.fail(data);
                } else {
                    layer.msg(data._msg, {icon: 2, time: 3000});
                }
            }
        },
        complete: function (xhr, ts) {
            // 请求完成后回调函数
            if (param.isLoading) {
                layer.close(index);
            }
            if (typeof param.complete == "function") {
                param.complete();
            }
        },
        error: function (xhr, textStatus) {
            layer.msg(textStatus + "请求失败...", {icon: 5, time: 3000});
        }
    });
}

/**
 * 加载Markdown编辑器
 *
 * @param data      内容
 * @param operation 操作
 * @returns {*}
 */
function loadEditor(data, operation) {
    return editormd("editormd", {
        width: "100%",
        height: 630,
        path: '/static/plugins/editor-md/lib/',
        theme: "default",
        previewTheme: "default",
        editorTheme: "default",
        markdown: data,
        codeFold: true,
        //syncScrolling : false,
        saveHTMLToTextarea: true,    // 保存 HTML 到 Textarea
        searchReplace: true,
        //watch : false,                // 关闭实时预览
        htmlDecode: "style,script,iframe|on*",            // 开启 HTML 标签解析，为了安全性，默认不开启
        //toolbar  : false,             //关闭工具栏
        //previewCodeHighlight : false, // 关闭预览 HTML 的代码块高亮，默认开启
        emoji: true,
        taskList: true,
        tocm: true,         // Using [TOCM]
        tex: true,                   // 开启科学公式TeX语言支持，默认关闭
        flowChart: true,             // 开启流程图支持，默认关闭
        sequenceDiagram: true,       // 开启时序/序列图支持，默认关闭,
        //dialogLockScreen : false,   // 设置弹出层对话框不锁屏，全局通用，默认为true
        //dialogShowMask : false,     // 设置弹出层对话框显示透明遮罩层，全局通用，默认为true
        //dialogDraggable : false,    // 设置弹出层对话框不可拖动，全局通用，默认为true
        //dialogMaskOpacity : 0.4,    // 设置透明遮罩层的透明度，全局通用，默认值为0.1
        //dialogMaskBgColor : "#000", // 设置透明遮罩层的背景颜色，全局通用，默认为#fff
        // 图片上传
        imageUpload: true,
        imageFormats: ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
        imageUploadURL: "/admin/api/img/upload",
        onload: function () {
            // 只读
            if("view" == operation) {
                $("#submit").hide();
                this.config({"readOnly": true});
                this.previewing();
            }
        }
    });
}

/**
 * layer 模态窗口
 *
 * @param title     标题
 * @param area      尺寸
 * @param content   内容
 */
function layerModal(title, area, content) {
    layer.open({
        type: 2,
        title: title,
        area: area,
        shade: 0.6,
        shadeClose: false,
        resize: false,
        content: content,
        scrollbar: false
    });
}

/**
 * layer 全屏模态窗口
 *
 * @param title     标题
 * @param content   内容
 */
function layerFullScreenModal(title, content) {
    let index = layer.open({
        type: 2,
        title: title,
        content: content,
    });
    layer.full(index);
}

/**
 * 复选框是否全选
 *
 * @param selector  选择器
 * @returns {boolean}
 */
function isCheck(selector) {
    let flag = true;
    $("" + selector + " :checkbox").each(function(){
        if(!$(this).is(":checked")) {
            flag = false;
            return flag;
        }
    });
    return flag;
}

/**
 * 获取复选框选中的值
 *
 * @param selector 选择器
 * @returns {Array}
 */
function checkVal(selector) {
    let values = [];
    $("" + selector + " :checkbox").each(function(){
        if($(this).is(":checked")) {
            values.push($(this).val());
        }
    });
    return values;
}

/**
 * 获取 zTree 当前被选中的节点数据集合
 *
 * @param selector 选择器
 * @returns {*}
 */
function getCheckedNodes(selector) {
    var treeObj = $.fn.zTree.getZTreeObj(selector);
    return treeObj.getCheckedNodes(true);
}

/**
 * zTree 全部选中/取消
 *
 * @param selector  选择器
 * @param flag      boolean
 */
function checkAllNodes(selector, flag) {
    let treeObj = $.fn.zTree.getZTreeObj(selector);
    treeObj.checkAllNodes(flag);
}

/**
 * 加载树形
 *
 * @param selector  选择器
 * @param zNodes    ZTree 数据
 */
function loadMenuTree(selector, zNodes) {
    if (null === zNodes || 0 >= zNodes.length) {
        $(selector).html("<li class='layui-col-md4' style='float: left; list-style: none;'>记录不存在...</li>");
        return false;
    }
    // 设置属性
    let setting = {
        check: {
            enable: true,
            chkboxType: {"Y": "ps", "N": "ps"}
        },
        data: {
            simpleData: {
                enable: true
            }
        }
    };
    // 初始化树形结构
    $.fn.zTree.init($(selector), setting, zNodes);
}

/**
 * 正则表达式获取请求URL上的参数
 *
 * @param paramName 请求参数名
 * @returns {*}     请求Value
 */
function getQueryString(paramName) {
    var reg = new RegExp("(^|&)" + paramName + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return decodeURI(r[2]);
    }
    return null;
}