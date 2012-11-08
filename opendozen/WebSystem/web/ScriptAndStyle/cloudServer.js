$(function () {
    $("#TestConnect").bind("click", function () {
        alert("hello world");
        TestConnect();
    })
})


function TestConnect()
{
    var postData = {};
    postData.data = "hello";
    postData.success = function (backData) {
        $(".responseRegion").html(backData);
    }
    AjaxConnect(postData);
    $(".responseRegion").html("正在等待响应.....");
}