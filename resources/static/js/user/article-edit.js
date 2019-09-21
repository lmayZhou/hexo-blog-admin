$(function () {
    // 格式化时间
    moment.locale(window.navigator.userLanguage || window.navigator.language);

    var editor;
    var request_url = "";
    var fileName = $("#fileName").val();
    if(fileName != "None" && fileName.length > 0) {
        request_url = "/admin/article/load/" + fileName + ".md";
    }

    if(request_url) {
        ajaxRequest({
            type: "GET",
            url: request_url,
            data: null,
            dataType: "json",
            isLoading: true,
            success: function (result) {
                editor = loadEditor(result._data, operation);
            }
        });
    } else {
        let data = "---\n" +
            "title: \n" +
            "date: " + moment().format("YYYY-MM-DD HH:mm:ss") + "\n" +
            "categories: \n" +
            "author: " + author + "\n" +
            "tags:\n" +
            "    - \n" +
            "cover_picture: \n" +
            "top: 1\n" +
            "---\n";
        editor = loadEditor(data, operation);
    }

    // 提交
    $("#submit").click(function() {
        let form = $("#editor-form").serialize();
        ajaxRequest({
            type: "POST",
            url: "/admin/article/edit.md",
            data: form,
            dataType: "json",
            isLoading: true,
            success: function (result) {
                layer.msg(result._msg, {time: 2000, icon: 6}, function () {
                    window.location.href = result._data;
                });
            }
        });
    });

    $("#go-back").click(function() {
        window.location.href = "/admin/articles.html";
    });
});