document.addEventListener('DOMContentLoaded', function () {
    const container = document.querySelector('.container');
    const leftImage = document.querySelector('.left-image');
    const rightImage = document.querySelector('.right-image');
    const splitter = document.querySelector('.splitter');
    const splitterWidth = parseFloat(getComputedStyle(splitter).width);

    container.addEventListener('mousemove', function (event) {
        const containerRect = container.getBoundingClientRect();
        const mouseX = event.clientX - containerRect.left;
        const percentage = mouseX / containerRect.width;

        // 更新splitter的位置  
        splitter.style.left = `${percentage * 100}%`;

        // 更新clip-path的值  
        const leftClip = `${(1 - percentage) * 100}%`;
        const rightClip = `${percentage * 100}%`;
        leftImage.style.clipPath = `inset(0 ${leftClip} 0 0)`;
        rightImage.style.clipPath = `inset(0 0 0 ${rightClip})`;
    });

    container.addEventListener('touchmove', function (event) {

        const containerRect = container.getBoundingClientRect();
        const touchX = event.touches[0].clientX - containerRect.left;
        const percentage = touchX / containerRect.width;

        // 更新splitter的位置  
        splitter.style.left = `${percentage * 100}%`;

        // 更新clip-path的值  
        const leftClip = `${(1 - percentage) * 100}%`;
        const rightClip = `${percentage * 100}%`;
        leftImage.style.clipPath = `inset(0 ${leftClip} 0 0)`;
        rightImage.style.clipPath = `inset(0 0 0 ${rightClip})`;

    });


    // 获取所有的图片行中的图片  
    var imagesInRow = document.querySelectorAll('.image-row img');
    // 获取需要替换 src 的图片  
    var leftImagesrc = document.querySelector('.image.left-image');
    var rightImagesrc = document.querySelector('.image.right-image');

    var overlay = document.getElementById('overlay');
    // 为每一张图片添加点击事件监听器  

    imagesInRow.forEach(function (image) {


        image.addEventListener('click', function () {
            imagesInRow.forEach(function (image) {
                image.style.border = "";
            })
            overlay.style.display = 'flex';
            setTimeout(function () {
                overlay.style.display = 'none';
                image.style.border = '2px solid #000';
                leftImagesrc.src = image.src;
                rightImagesrc.src = image.src.replace('pixelopen_demo', 'pixelopen_black_and_white_demo');
            }, 500);
        });
    });


    // 点击上传
    document.getElementById("upload-image-btn").addEventListener("click", function () {
        upload_image()
    });
    document.getElementById("upload-image-btn2").addEventListener("click", function () {
        upload_image()
    });
    document.getElementById("upload-image-btn4").addEventListener("click", function () {
        upload_image()
    });
    document.getElementById("upload-image-btn3").addEventListener("click", function () {
        originimage = document.getElementById('result-left-image').src;
        resultimage = document.getElementById('result-right-image').src;
        window.open(`/editor/whitelogo/?originimage=${originimage}&resultimage=${resultimage}`, '_blank');
    });

    // 拖拽上传
    const dropzone = document.getElementById('upload-image-btn');

    // 当拖拽在目标区域内移动时  
    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault(); // 允许放置  
        dropzone.style.backgroundColor = "#e2e2e2";
    });

    // 当拖拽离开目标区域时  
    dropzone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropzone.style.backgroundColor = "";
    });

    // 当拖拽结束时（在目标区域内释放）  
    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.style.backgroundColor = "";
        const formData = new FormData();

        const file = e.dataTransfer.files[0];
        formData.append('file', file);
        fetchReverseImage(formData);

    });

    // // 禁止画布移动
    // document.getElementById('upload-image-btn3').addEventListener('touchmove', function (event) {
    //     event.preventDefault();
    // });
})

function fetchReverseImage(formData) {
    // 添加必要的CSRF令牌（如果有）  
    const csrftoken = getCookie('csrftoken');
    if (csrftoken) {
        formData.append('X-CSRFToken', csrftoken);
    } else {
        console.warn('CSRF token not found!');
    }

    // 使用fetch发送POST请求  
    fetch('upload-image/whitelogo/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // 处理后端返回的数据  
            document.getElementById('result-left-image').src = data["left-image"];
            document.getElementById('result-right-image').src = data["right-image"];
            document.getElementById('overlay').style.display = 'none';
            moveToElement(); // 假设这是您定义的一个函数  
        })
        .catch(error => {
            console.error('Error uploading file:', error);
        });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function moveToElement() {
    // 获取目标元素  
    var targetElement = document.getElementById('ok-front-main-title');

    // 使用 scrollIntoView 方法，可以添加选项来控制滚动行为  
    targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' })
}


function upload_image() {
    var isClick = true;
    // 弹窗上传文件  
    var input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";
    input.style.display = 'none'; // 隐藏文件输入  
    document.body.appendChild(input); // 将输入添加到文档中（尽管它是隐藏的）  

    input.addEventListener("change", function () {
        document.getElementById('overlay').style.display = 'flex';

        var file = input.files[0];
        if (isClick) {
            isClick = false;
            setTimeout(function () {
                isClick = true;
            }, 3000); // 重置点击标志，可能用于防止重复上传  

            if (file && file.type.startsWith("image/")) {
                // 不需要读取文件为数据URL，直接发送文件  
                var formData = new FormData();
                formData.append('file', file);

                // 使用fetch API发送POST请求  
                fetch('upload-image/whitelogo/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                })
                    .then(response => response.json())
                    .then(data => {
                        // console.log('Success:', data);
                        document.getElementById('result-left-image').src = data["left-image"];
                        document.getElementById('result-right-image').src = data["right-image"];
                        document.getElementById('overlay').style.display = 'none';
                        moveToElement();
                    })
                    .catch(error => {
                        console.error('Error:', error);

                    });
            } else {

                alert("Please select an image file.");
            }


            document.body.removeChild(input);
        } else {

            alert("Don't upload again within 3 seconds.");
        }
    });

    // 触发文件输入元素的点击事件  
    input.click();
}
