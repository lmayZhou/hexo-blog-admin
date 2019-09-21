$(function () {
    // 格式化时间
    moment.locale(window.navigator.userLanguage || window.navigator.language);

    ajaxRequest({
        type: "GET",
        url: "/admin/articles/load",
        data: {
            pageNumber: 1,
            pageSize: 5,
            sortName: "_id",
            sortOrder: "desc"
        },
        dataType: "json",
        isLoading: true,
        success: function (result) {
            $.each(result._data._rows, function(idx, item) {
                let li = "";
                if(idx === 0) {
                    li += "<li class='work'>" +
                        "   <input class='radio' id='work" + idx + "' name='works' type='radio' checked>" +
                        "   <div class='relative'>" +
                        "       <label for='work" + idx + "'>" + item._title + "</label>" +
                        "       <span class='date'>" + moment.utc(item._date).format("YYYY-MM-DD HH:mm:ss") + "</span>" +
                        "       <span class='circle'></span>" +
                        "   </div>" +
                        "   <div class='content'>" +
                        "       <p>" +
                                    "Tags:&nbsp;&nbsp;" + item._tags + "<br/>" +
                                    "Categories:&nbsp;&nbsp;" + item._categories + "<br/>" +
                                    "Author:&nbsp;&nbsp;" + item._author + "<br/>" +
                        "       </p>" +
                        "   </div>" +
                        "</li>";
                } else {
                    li = "<li class='work'>" +
                        "   <input class='radio' id='work" + idx + "' name='works' type='radio'>" +
                        "   <div class='relative'>" +
                        "       <label for='work" + idx + "'>" + item._title + "</label>" +
                        "       <span class='date'>" + moment.utc(item._date).format("YYYY-MM-DD HH:mm:ss") + "</span>" +
                        "       <span class='circle'></span>" +
                        "   </div>" +
                        "   <div class='content'>" +
                        "       <p>" +
                                    "Tags:&nbsp;&nbsp;" + item._tags + "<br/>" +
                                    "Categories:&nbsp;&nbsp;" + item._categories + "<br/>" +
                                    "Author:&nbsp;&nbsp;" + item._author + "<br/>" +
                        "       </p>" +
                        "   </div>" +
                        "</li>";
                }
                $("#timeline").append(li);
            });
        }
    });
});
