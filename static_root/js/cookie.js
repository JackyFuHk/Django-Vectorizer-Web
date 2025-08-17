document.addEventListener('DOMContentLoaded', function () {
    if (getCookie('accept_cookie') == null) {
        document.getElementsByClassName('ok-cookie-container')[0].style.display = "flex";
    }
})

document.addEventListener('DOMContentLoaded', function () {
    var acceptButton = document.querySelector('.ok-accept-cookie');
    if (acceptButton) {
        acceptButton.addEventListener('click', function () {
            hideCookieConsent();
            setCookie("accept_cookie", "true", 365, '/');
        });
    } else {
        console.error('未找到接受Cookie的按钮');
    }
});

function hideCookieConsent() {
    var cookieConsent = document.querySelector('.ok-cookie-container');
    cookieConsent.style.display = 'none'; // 隐藏Cookie窗口  
}


function setCookie(name, value, days = 365, path = '/') {
    let expires = '';
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = `; expires=${date.toUTCString()}`;
    }
    document.cookie = `${name}=${encodeURIComponent(value)}${expires}; path=${path}`;
}

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$&') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : null;
}