$(function () {
    var editor;
    ajaxRequest({
        type: "GET",
        url: "/admin/about-me/load.md",
        data: null,
        dataType: "json",
        isLoading: true,
        success: function (result) {
            editor = loadEditor(result._data, operation);
        }
    });

    // 提交
    $("#submit").click(function() {
        var form = $("#editor-form").serialize();
        ajaxRequest({
            type: "POST",
            url: "/admin/about-me/edit.md",
            data: form,
            dataType: "json",
            isLoading: true,
            success: function (result) {
                layer.msg(result._msg, {time: 2000, icon: 6}, function () {
                    window.location.reload();
                });
            }
        });
    });
});