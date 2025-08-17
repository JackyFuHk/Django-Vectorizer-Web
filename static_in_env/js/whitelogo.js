let is_auth = false;
let index = 0;
document.addEventListener('DOMContentLoaded', function () {

    // 先看有没有历史
    if (imageHistoryData !== undefined && (typeof imageHistoryData === 'string' ? imageHistoryData.trim() !== '' : imageHistoryData.length > 0)) {
        document.getElementById('allhistory').style.display = 'flex';
        document.getElementById('allhistoryh2').style.display = 'flex';
        document.getElementById('other-option-upload').style.display = 'flex';

        for (ii = 0; ii < imageHistoryData.length; ii++) {
            imgsrc = imageHistoryData[ii].imgsrc
            index = imageHistoryData[ii].index
            imgname = imageHistoryData[ii].imgname
            addicon(imgsrc, imgname, ii);
        }
        setTimeout(function () {
            for (ii = 0; ii < imageHistoryData.length; ii++) {
                document.getElementById('btn' + ii).innerHTML = "点击下载";
                document.getElementById('status' + ii).innerHTML = "转换完成";
                document.getElementById('btn' + ii).value = 1;
                document.getElementById('progressbar' + ii).style.width = "100%";
            }
        }, 2500)
        index = imageHistoryData.length - 1;
    }

    document.getElementById("upload-image-btn").addEventListener('click', function () {

        upload_image();
    })
    const container2 = document.getElementById('upload-image-btn3');
    const observerOptions = {
        root: null, // 使用视口作为根元素  
        rootMargin: '0px',
        threshold: 0.5 // 当元素50%可见时触发  
    };
    const observerCallback = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {

                // 停止观察，因为动画已经触发  
                observer.unobserve(container2);
            }
        });
    };


    const observer = new IntersectionObserver(observerCallback, observerOptions);
    observer.observe(container2);

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

        var leftClip_new = normalizeToRange((1 - percentage) * 100, 0, 100, scale = 1);
        var rightClip_new = normalizeToRange(percentage * 100, 0, 100, scale = 1);

        leftImage.style.clipPath = `inset(0 ${leftClip_new} 0 0)`;
        rightImage.style.clipPath = `inset(0 0 0 ${rightClip_new})`;
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


        var leftClip_new = normalizeToRange((1 - percentage) * 100, 0, 100, scale = 1);
        var rightClip_new = normalizeToRange(percentage * 100, 0, 100, scale = 1);

        leftImage.style.clipPath = `inset(0 ${leftClip_new} 0 0)`;
        rightImage.style.clipPath = `inset(0 0 0 ${rightClip_new})`;

    });


    // 获取所有的图片行中的图片  
    var imagesInRow = document.querySelectorAll('#image-row img');
    // 获取需要替换 src 的图片  
    var leftImagesrc = document.querySelector('.image.left-image');
    var rightImagesrc = document.querySelector('.image.right-image');
    // 为每一张图片添加点击事件监听器  
    var overlay = document.getElementById('overlay');
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
                rightImagesrc.src = image.src.replace('demo', 'black_and_white_demo');
            }, 1200);
        });
    });

})

function showMessage(msg) {
    var messageContainer = document.getElementById('message-container');
    messageContainer.style.display = 'block'; // 显示容器
    messageContainer.innerHTML = msg
    // 设置3秒后隐藏容器
    setTimeout(function () {
        messageContainer.style.display = 'none';
    }, 10000);
}
function normalizeToRange(value, inputMin, inputMax, scale) {
    var step = 50 / scale;
    var outputMin = 50 - step;
    var outputMax = 50 + step;

    // 确保输入值在输入范围内  
    if (value < inputMin - 1 || value > inputMax + 1) {
        throw new Error(`Value ${value} is out of the input range [${inputMin}, ${inputMax}]`);
    }

    // 使用线性插值公式计算归一化后的值  

    var Clip_new = ((value - inputMin) * (outputMax - outputMin)) / (inputMax - inputMin) + outputMin
    return `${Clip_new}%`
}
function addicon(imgsrc, imgname, index) {

    const authority = is_authority();

    const all_history = document.getElementById('allhistory')

    const hisdiv = document.createElement('div');
    hisdiv.id = "pngtosvghistory" + index;
    hisdiv.className = 'history-container'
    all_history.append(hisdiv)

    const upload_history = document.getElementById('pngtosvghistory' + index)

    // 创建 img 元素  
    const img = document.createElement('img');
    img.src = imgsrc;
    img.alt = `jpg icon`;
    img.style.width = '120px';
    img.className = 'animated-image2';
    img.id = "image" + index

    upload_history.appendChild(img);

    const p = document.createElement('div');
    p.innerHTML = "上传中.."
    p.id = "status" + index
    p.style.float = 'left'

    upload_history.appendChild(p);

    // 创建进度条容器  
    const progressBarContainer = document.createElement('div');
    progressBarContainer.className = 'progress-bar-container';

    // 创建进度条元素  
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    progressBar.id = 'progressbar' + index
    progressBar.style.width = '0%';
    setTimeout(function () {
        progressBar.style.width = '50%';
        p.innerHTML = "上传完成.."
    }, 1500);

    // 将进度条添加到进度条容器中  
    progressBarContainer.appendChild(progressBar);
    // 将div添加到容器中
    upload_history.appendChild(progressBarContainer);

    const div = document.createElement('div');
    div.id = "btn" + index
    div.data = imgname
    div.innerText = `点击转换`;
    div.className = "upload-btn"
    div.value = 0
    div.addEventListener('click', function () {
        transfer_svg(imgsrc, index, imgname)
    });
    setTimeout(function () {
        div.click();
    }, 1000);
    // 将div添加到容器中
    upload_history.appendChild(div);


}

async function is_authority() {
    const response = await fetch('/is_subscription/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
    });

    // 检查响应状态是否正常（200-299）
    if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
    }

    // 解析响应体为 JSON
    const data = await response.json();

    is_auth = data['is_auth'];
    return data['is_auth']; // 返回解析后的数据中的is_auth字段
}

async function transfer_svg(imgsrc, index, imgname) {
    is_authority();
    // 如果已经登录，可以运行。
    if (is_auth == false) {
        showMessage('请先登录后免费使用哦~')
    }
    else {
        // 判断是否已经转换完成
        const is_ok = document.getElementById('btn' + index).value;
        if (is_ok == 1) {
            fetch(`/whitelogo_download_svg/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'), // 如果你的Django项目启用了CSRF保护  
                },
                body: JSON.stringify({
                    "name": imgname,
                    "imgsrc": imgsrc,
                    "index": index
                }),
            })
                .then(response => response.json())
                .then(data => {
                    var base64String = data['data']
                    // console.log(base64String)
                    const byteString = atob(base64String.split(',')[1]);
                    const mimeString = base64String.split(',')[0].split(':')[1].split(';')[0]; // 获取MIME类型，例如"image/png"
                    const ab = new ArrayBuffer(byteString.length);
                    const ia = new Uint8Array(ab);
                    for (let i = 0; i < byteString.length; i++) {
                        ia[i] = byteString.charCodeAt(i);
                    }

                    // 创建Blob对象
                    const blob = new Blob([ab], { type: mimeString });

                    // 创建一个指向该Blob对象的URL
                    const url = URL.createObjectURL(blob);

                    // 创建一个隐藏的<a>标签并设置其属性
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = imgname + '.png'; // 根据需要设置文件扩展名
                    document.body.appendChild(a); // 需要添加到DOM中才能触发点击事件（在某些浏览器中）
                    a.click();

                    // 释放URL对象并从DOM中移除<a>标签
                    URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
        else {
            document.getElementById('status' + index).innerHTML = "正在处理中...";
            document.getElementById('btn' + index).innerHTML = "正在处理";
            try {
                // 使用 fetch API 发送 POST 请求    
                const response = await fetch('/whitelogo/', {
                    method: 'POST',
                    body: JSON.stringify({
                        "imgsrc": imgsrc,
                        "index": index,
                        "name": imgname
                    }),
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'), // 如果你的Django项目启用了CSRF保护  
                    },
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();

                document.getElementById('progressbar' + index).style.width = "100%";
                document.getElementById('btn' + index).innerHTML = "点击下载";
                document.getElementById('status' + index).innerHTML = "转换完成";
                document.getElementById('btn' + index).value = 1;
                // console.log('Success for file ' + (i + 1) + ':', data);

                // 添加停顿  
                await new Promise(resolve => setTimeout(resolve, 1000)); // 1秒停顿  

            } catch (error) {
                console.error('Error for file ' + (i + 1) + ':', error);
            }
        }
    }
}



async function upload_image() {
    // 弹窗上传文件      
    var input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";
    input.multiple = true; // 允许选择多个文件    
    input.style.display = 'none'; // 隐藏文件输入      
    document.body.appendChild(input); // 将输入添加到文档中（尽管它是隐藏的）    

    input.addEventListener("change", async function () {
        document.getElementById('allhistory').style.display = 'flex';
        document.getElementById('allhistoryh2').style.display = 'flex';
        document.getElementById('other-option-upload').style.display = 'flex';

        // 获取 upload-image-btn 元素    
        const uploadButton = document.getElementById('upload-image-btn');

        var files = input.files;
        var maxFiles = 10; // 允许的最大文件数量    
        if (files.length > 0) {
            var uploadFiles = Array.from(files); // 将 FileList 转换为数组    

            // 逐个异步上传文件    
            for (let i = 0; i < uploadFiles.length && i < maxFiles; i++) {
                const file = uploadFiles[i];
                if (file.type.startsWith("image/")) {
                    // 创建 FormData 对象并添加文件    
                    var formData = new FormData();
                    formData.append('file', file);
                    var reader = new FileReader();

                    // 读取文件为 DataURL（即 Base64 编码的字符串）  
                    reader.readAsDataURL(file);

                    try {
                        // 使用 fetch API 发送 POST 请求    
                        const response = await fetch('/upload-image/', {
                            method: 'POST',
                            body: formData,
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken')
                            },
                        });

                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }

                        const data = await response.json();


                        addicon(data["user_png"], data['name'], index)
                        index += 1
                        // document.getElementById('svg' + data['name']).style.width = "30%";
                        // document.getElementById('btn' + data['name']).style.opacity = 1;


                        // console.log('Success for file ' + (i + 1) + ':', data);

                        // 添加停顿  
                        await new Promise(resolve => setTimeout(resolve, 1000)); // 1秒停顿  

                    } catch (error) {
                        console.error('Error for file ' + (i + 1) + ':', error);
                    }
                } else {
                    console.warn('Skipped non-image file:', file.name);
                }
            }
        } else {
            alert("No files selected.");
        }
    });

    // 触发文件输入元素的点击事件      
    input.click();
}



