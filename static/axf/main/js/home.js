$(function () {
    ISpr();
ISprMenu();
})

function ISpr() {
    var swiper = new Swiper("#topSwiper", {
            loop: true,
            autoplay: 3000,
            pagination: '.swiper-pagination'
        }
    );
}
function ISprMenu() {
    var swiper = new Swiper("#swiperMenu", {
           slidesPerView: 3,
        }
    );
}