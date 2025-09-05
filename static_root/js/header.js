document.addEventListener('DOMContentLoaded', function () {
    // document.getElementById('loginButton').addEventListener('click', function () {
    //     window.location.href = 'https://open.weixin.qq.com/connect/qrconnect?appid=wx16d87b4275f88ca4&redirect_uri=https%3A%2F%2Fwww.vectorizer.cn%2Fwechat%2Fcallback&response_type=code&scope=snsapi_login#wechat_redirect'
    // })
    // updateButtonVisibility();  // var activeLink = localStorage.getItem('activeLink');
    // if (activeLink) {
    //     var links = document.querySelectorAll('.ok-nav-link[href="' + activeLink + '"]');
    //     if (links.length) {
    //         links.forEach(function (link) {
    //             link.classList.add('active');
    //             // 注意：这里你可能还需要修改链接的href属性，以便在点击时实际跳转到对应的URL  
    //             // 但在这个简单的示例中，我们不会这样做  
    //         });
    //     }
    // }

    // document.querySelectorAll('.ok-nav-link').forEach(function (link) {
    //     link.addEventListener('click', function (e) {
    //         e.preventDefault(); // 阻止链接的默认跳转行为  
    //         // 清除之前设置的active类  
    //         document.querySelectorAll('.ok-nav-link.active').forEach(function (activeLink) {
    //             activeLink.classList.remove('active');
    //         });

    //         // 设置当前链接为active  
    //         this.classList.add('active');

    //         // 存储当前激活的链接的data-href属性到LocalStorage  
    //         localStorage.setItem('activeLink', this.getAttribute('href'));

    //         // 这里你可以使用window.location.href = this.getAttribute('data-href'); 来实际跳转到链接指向的页面  
    //         // 但在这个示例中，我们不会这样做，因为这会导致页面跳转并丢失激活状态  
    //     });
    // });

    // 购物车icon的hover颜色
    // var cartElement = document.getElementById("cartbanner");
    // cartElement.addEventListener("mouseenter", function () {
    //     var rectElement = document.getElementById("myRect");
    //     rectElement.setAttribute("fill", "#FFCB8E");
    // });
    // cartElement.addEventListener("mouseleave", function () {
    //     var rectElement = document.getElementById("myRect"); rectElement.setAttribute("fill", "");
    // });

    // account的icon
    var allCookies = document.cookie;
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }



    // 移动端弹窗事件
    $(document).ready(function () {
        // 为按钮绑定点击事件，以切换弹窗的显示状态  
        $('#ok-navbar-toggler').click(function (e) {
            e.stopPropagation(); // 阻止事件冒泡到文档上（可选，但在这里可能不是必需的，取决于其他逻辑）  
            $('.ok-navbar-collapse').toggleClass('show');
        });

        // 使用事件委托来监听除了弹窗本身以外的点击事件  
        $(document).on('click', function (e) {
            // 检查点击的目标元素或其任何父元素是否不是.ok-navbar-collapse  
            if (!$(e.target).closest('.ok-navbar-collapse').length) {
                // 如果不是，隐藏弹窗  
                $('.ok-navbar-collapse').removeClass('show');
            }
        });

        // 这一步实际上是可选的，因为我们已经阻止了事件冒泡到文档上（在弹窗内部点击时）  
        // 但为了清晰起见，我还是保留了它，表明我们有意为之  
        $('.ok-navbar-collapse').click(function (e) {
            e.stopPropagation(); // 阻止事件冒泡到文档上，这样点击弹窗内部时不会触发隐藏  
        });
    });




});

function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}


