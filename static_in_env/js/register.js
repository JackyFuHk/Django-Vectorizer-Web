
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('sendCode').addEventListener('click', function () {
        const emailInput = document.getElementById('email').value;

        if (isValidEmail(emailInput)) {
            document.getElementById('warning').innerHTML = '验证码已发送';

            fetch('send_certification/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ email: emailInput })
            })
                .then(response => response.json())
                .then(data => {

                })
                .catch(error => {
                    console.error('Error:', error);

                });
        } else {
            document.getElementById('warning').innerHTML = '邮箱不正确';
        }
    })
    document.getElementById('submit').addEventListener('click', function () {
        // // 获取密码字段  
        var password1 = document.getElementById('password').value;
        // var password2 = document.getElementById('confirmPassword').value;
        var email = document.getElementById('email').value;
        var code = document.getElementById('verificationCode').value
        // 检查两次密码是否一致  
        // if (email.length != 11) {
        //     // 如果不一致，显示错误消息并阻止表单提交  
        //     document.getElementById('warning').innerHTML = "";
        // }
        // else {
        //     console.log(email, code)
        fetch('create_user/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                email: email,
                password: "111",
                code: code,
            })
        })
            .then(response => response.json())
            .then(data => {
                // console.log(data)
                if (data.code == '200') {
                    window.location.href = '/'
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        // }

    })
})

function isValidEmail(email) {
    // 使用正则表达式验证电子邮件地址  
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return false;
}