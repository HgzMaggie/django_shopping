a = "0";

// 点击事件的绑定
$(function () {

    // 展示：全部类型，并收起：综合排序
    the_slideDown("#all_types", "#all_cer", "#sort_rule", "#sort_cer");
    // 收起：全部类型
    the_slideUp("#all_types", "#all_cer",);

    // 展示：综合排序，并收起：全部类型
    the_slideDown("#sort_rule", "#sort_cer", "#all_types", "#all_cer");
    // 收起：综合排序
    the_slideUp("#sort_rule", "#sort_cer",);

    $(".subShopping").click(function () {
        var $sub = $(this);

        // attr获取html标签的属性
        var goodsid = $sub.attr("goodsid");

        $.get('/axf/subtocart/', {'goodsid': goodsid}, function (data) {
            console.log(data);
            if (data['status'] === 302) {
                window.open('/axf/login/', target = "_self");
            } else if (data["status"] === 200) {
                console.log('减一成功');
                // $add.next('span')找到.subShopping下面最近的span
                $sub.next('span').html(data['C_goods_num']);
            } else if (data['msg']=== 0){
                console.log('里面没有数据');
            }
        });
    });
    $(".addShopping").click(function () {
        var $add = $(this);

        // attr获取html标签的属性
        var goodsid = $add.attr("goodsid");

        $.get('/axf/addtocart/', {'goodsid': goodsid}, function (data) {
            console.log(data);
            if (data['status'] === 302) {
                window.open('/axf/login/', target = "_self");
            } else if (data["status"] === 200) {
                console.log('添加成功');
                // $add.prev('span')找到.addShopping上面最近的span
                $add.prev('span').html(data['C_goods_num']);
            }
        });
    });
});


// the_text:当前点击的文字  the_shade:当前阴影

// 展示
function the_slideDown(the_text, the_shade, other_text, other_shade) {
    $(the_text).click(function () {
        var $the_shade = $(the_shade);

        // 先检查如果当前id已经被点击过了，就视为收起执行
        if (a === the_text) {
            $the_shade.slideUp();
            the_chevron(the_text, "glyphicon-chevron-up", "glyphicon-chevron-down");
            a = "0";

        // 否则展示
        } else {
            // 显示阴影
            $the_shade.slideDown();
            the_chevron(the_text, "glyphicon-chevron-down", "glyphicon-chevron-up");
            var $other_shade = $(other_shade);
            $other_shade.slideUp();
            the_chevron(other_text, "glyphicon-chevron-up", "glyphicon-chevron-down");
            // 记录当前id已经被点击
            a = the_text;
        }

    })
}

// 收起
function the_slideUp(the_text, the_shade) {

    $(the_shade).click(function () {
        // 点击阴影，收回阴影
        var $the_shade = $(the_shade);
        $the_shade.slideUp();
        the_chevron(the_text, "glyphicon-chevron-up", "glyphicon-chevron-down");
        // 清除点击记录
        a = "0"
    })
}


// 改变V形符号，向上向下
function the_chevron(the_text, the_rem, the_add) {
    var $the_text = $(the_text);
    var $span = $the_text.find("span").find("span");
    $span.removeClass(the_rem).addClass(the_add);
}
