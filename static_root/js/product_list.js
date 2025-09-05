document.addEventListener('DOMContentLoaded', function () {
    // 获取所有的ok-productlist-gallery容器  
    const galleries = document.querySelectorAll('.ok-productlist-gallery');

    // 为每个容器添加事件监听器（实际上这里我们不需要为容器本身添加点击事件，而是为里面的图片添加）  
    galleries.forEach(gallery => {
        // 获取当前容器的id（注意，这里假设id是唯一的，并且是数字）  
        const galleryId = gallery.id;

        // 获取当前容器内的所有图片  
        const images = gallery.querySelectorAll('.ok-productlist-gallery-image');

        // 为每张图片添加点击事件监听器  
        images.forEach((img, index) => {
            img.addEventListener('click', function (event) {
                const imgSrc = this.src;
                const imgAlt = this.alt;
                // // 这里的index就是图片在当前容器中的索引（从0开始）  
                // console.log(`在id为${galleryId}的容器中，你点击了第${index + 1}张图片，其src为：${imgSrc}`);
                // 把主图换掉
                // 选取所有具有ok-productlist-image类的元素  
                var main_images = document.querySelectorAll('.ok-productlist-image');

                // 遍历这些元素  
                main_images.forEach(function (main_image) {
                    // 检查元素的id是否为1  
                    if (main_image.id == galleryId) {
                        main_image.src = imgSrc;
                        main_image.alt = imgAlt;
                    }
                });
            });
        });
    });

    // 显示tag

    if (window.innerWidth > 990) {

        document.querySelectorAll('.ok-productlist-container').forEach(function (element) {
            element.addEventListener('mouseenter', function () {
                Array.from(this.querySelectorAll('.ok-productlist-tag')).forEach(function (ok2Element) {
                    ok2Element.style.display = 'inline-block';
                });
            });

            element.addEventListener('mouseleave', function () {
                Array.from(this.querySelectorAll('.ok-productlist-tag')).forEach(function (ok2Element) {
                    ok2Element.style.display = 'none';
                });
            });
        });
    }


    // 点击分类筛选
    document.getElementById("product_category_all").addEventListener('click', function () {
        window.location.href = '/product/'
    });
    document.getElementById("product_category_recommend").addEventListener('click', function () {
        window.location.href = '/product-category/recommended/'
    });
    document.getElementById("product_category_food").addEventListener('click', function () {
        window.location.href = '/product-category/food/'
    });
    document.getElementById("product_category_drink").addEventListener('click', function () {
        window.location.href = '/product-category/drink/'
    });
    document.getElementById("product_category_bag").addEventListener('click', function () {
        window.location.href = '/product-category/bag/'
    });
    document.getElementById("product_category_utensils").addEventListener('click', function () {
        window.location.href = '/product-category/utensils/'
    });
    document.getElementById("product_category_other").addEventListener('click', function () {
        window.location.href = '/product-category/other/'
    });


    // 初始化筛选。
    if (window.location.pathname.includes('product-category')) {
        product_category_filter(getLastSlugFromUrl())
    }
})

function getLastSlugFromUrl() {
    // 获取当前URL的路径部分  
    const path = window.location.pathname;

    // 使用split('/')将路径分割成数组，并移除空字符串（例如，对于'/'开头的路径）  
    const segments = path.split('/').filter(Boolean);

    // 获取数组中的最后一个元素，即最后一个slug  
    const lastSlug = segments[segments.length - 1];

    return lastSlug;
}

function product_category_filter(product_category) {

    document.querySelectorAll('.ok-productlist-container').forEach(function (element) {

        if (element.id !== product_category) {
            element.style.display = 'none';
        }
        else {

            element.style.display = 'flex';
        }
    });
    if (product_category == "all") {
        document.querySelectorAll('.ok-productlist-container').forEach(function (element) {
            element.style.display = 'flex';
        });
    }
}