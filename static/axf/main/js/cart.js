$(function () {
    $(".confirm").click(function () {
        var $confirm = $(this);
        var $li = $confirm.parents("li");
        var cartid = $li.attr('cartid');
        $.getJSON("/axf/changecart/", {'cartid': cartid}, function (data) {
            console.log(data);
            if (data['status'] === 200) {
                if (data['C_is_select']) {
                    $confirm.find("span").find("span").html("√");

                } else {
                    $confirm.find("span").find("span").html("");
                }
            }
        });
    });
    $(".subShopping").click(function () {
        var $sub = $(this);
        var $li = $sub.parents("li");
        var goodsid = $li.attr("goodsid");
        $.get('/axf/subtocart/', {'goodsid': goodsid}, function (data) {
            console.log(data);
            if (data['status'] === 200) {
                if (data['C_goods_num'] > 0) {
                    $sub.next('span').html(data['C_goods_num']);
                } else {
                    $li.remove();
                }
            }
        });
    });
    $(".addShopping").click(function () {
        var $add = $(this);
        var $li = $add.parents("li");
        var goodsid = $li.attr("goodsid");
        $.get('/axf/addtocart/', {'goodsid': goodsid}, function (data) {
            if (data['status'] === 200) {
                $add.prev('span').html(data['C_goods_num']);
            }
        });
    });
});
