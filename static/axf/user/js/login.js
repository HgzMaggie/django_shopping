$(function () {
    $("img").click(function () {
        // 在浏览器里面路径不改变,这个图他就会不发生改变,所以给这个路径加一个随机数让浏览器知道改变了
        $(this).attr("src", "/axf/getcode/?t=" + Math.random());
        $("#verify_span").html("").css("color", "green");
    });
});

function parse_data() {

    var $password_input = $("#password_input");
    var password = $password_input.val().trim();
    $password_input.val(hex_md5(password));

    return true
}