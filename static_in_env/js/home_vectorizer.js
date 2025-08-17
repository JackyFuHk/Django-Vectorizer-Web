let uploadimageindex = 0
let is_auth = false;
document.addEventListener('DOMContentLoaded', function () {


    const container2 = document.getElementById('upload-image-btn3');
    const observerOptions = {
        root: null, // 使用视口作为根元素  
        rootMargin: '0px',
        threshold: 0.5 // 当元素50%可见时触发  
    };

    const observerCallback = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // 容器进入视口，添加zoomed类  
                container2.querySelectorAll('.right-image').forEach(image => {
                    image.classList.add('zoomed');
                });
                container2.querySelectorAll('.left-image').forEach(image => {
                    image.classList.add('zoomed');
                });
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

        var leftClip_new = normalizeToRange((1 - percentage) * 100, 0, 100, scale = 2);
        var rightClip_new = normalizeToRange(percentage * 100, 0, 100, scale = 2);

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


        var leftClip_new = normalizeToRange((1 - percentage) * 100, 0, 100, scale = 2);
        var rightClip_new = normalizeToRange(percentage * 100, 0, 100, scale = 2);

        leftImage.style.clipPath = `inset(0 ${leftClip_new} 0 0)`;
        rightImage.style.clipPath = `inset(0 0 0 ${rightClip_new})`;

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
            leftImagesrc.classList.remove('zoomed');
            rightImagesrc.classList.remove('zoomed');
            setTimeout(function () {
                overlay.style.display = 'none';
                image.style.border = '2px solid #000';
                leftImagesrc.src = image.src;
                rightImagesrc.src = image.src.replace('.png', '.svg');
                leftImagesrc.classList.add('zoomed');
                rightImagesrc.classList.add('zoomed');
            }, 1200);
        });
    });


    // 点击上传
    document.getElementById("upload-image-btn").addEventListener("click", handleUploadClick);
    document.getElementById("upload-image-btn2").addEventListener("click", handleUploadClick);
    document.getElementById("upload-image-btn4").addEventListener("click", handleUploadClick);
    // document.getElementById("upload-image-btn3").addEventListener("click", function () {
    //     originimage = document.getElementById('result-left-image').src;
    //     resultimage = document.getElementById('result-right-image').src;
    //     window.open(`/editor/pngtosvg/?svg=${resultimage}`, '_blank');
    // });

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
        // 获取 upload-image-btn 元素    
        const uploadButton = document.getElementById('upload-image-btn');

        // 隐藏 upload-image-btn 下的所有现有子元素（如果有的话）    
        Array.from(uploadButton.children).forEach(child => {
            child.style.display = 'none';
        });
        const file = e.dataTransfer.files;
        fetchReverseImage2(file);

    });

    // // 禁止画布移动
    // document.getElementById('upload-image-btn3').addEventListener('touchmove', function (event) {
    //     event.preventDefault();
    // });
})
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

function fetchReverseImage(formData) {
    // 添加必要的CSRF令牌（如果有）  
    const csrftoken = getCookie('csrftoken');
    if (csrftoken) {
        formData.append('X-CSRFToken', csrftoken);
    } else {
        console.warn('CSRF token not found!');
    }

    // 使用fetch API发送POST请求  
    fetch('upload-image/pngtosvg/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
        .then(response => response.json())
        .then(data => {
            // console.log('Success:', data);
            window.open(`/editor/pngtosvg/?svg=${data["user_png"]}`, '_blank');
        })
        .catch(error => {
            console.error('Error:', error);

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

function moveToElement(n) {
    // 获取目标元素  
    var targetElement = document.getElementById('ok-front-main-title');

    // 使用 scrollIntoView 方法，可以添加选项来控制滚动行为  
    targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
function handleUploadClick() {
    upload_image();
    // 移除监听器  
    document.getElementById("upload-image-btn").removeEventListener("click", handleUploadClick);
}
function addicon(imgsrc, name, index) {
    const authority = is_authority();
    const uploadButton = document.getElementById('upload-image-btn');
    // 添加 10 个 img 元素和对应的进度条  

    // 创建父容器 div  
    const parentContainer = document.createElement('div');
    parentContainer.className = 'image-and-progress-container'; // 可以为这个容器添加 CSS 类以便样式化  
    parentContainer.id = name;
    // 创建 img 元素  
    const img = document.createElement('img');
    img.src = imgsrc;
    img.alt = `jpg icon`;
    img.style.width = '120px';
    img.className = 'animated-image2'; // 假设你有一个对应的 CSS 类  

    // 创建进度条容器  
    const progressBarContainer = document.createElement('div');
    progressBarContainer.className = 'progress-bar-container';

    // 创建进度条元素  
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    progressBar.id = 'svg' + name
    progressBar.style.width = '0%'; // 初始宽度为 0%  

    // 将进度条添加到进度条容器中  
    progressBarContainer.appendChild(progressBar);

    // 将 img 和进度条容器添加到父容器中  
    parentContainer.appendChild(img);
    parentContainer.appendChild(progressBarContainer);

    // 下载button加入容器。
    const downloadButton = document.createElement('div');
    downloadButton.id = 'btn' + name
    downloadButton.innerHTML = 'download'
    downloadButton.className = 'download-button'
    parentContainer.addEventListener('click', function () {
        if (is_auth == false) {
            showMessage('请先登录后免费下载哦~')
        }
        else {
            fetch(`download_svg2/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'), // 如果你的Django项目启用了CSRF保护  
                },
                body: JSON.stringify({
                    "name": name
                }),
            })
                .then(response => response.json())
                .then(data => {

                    // console.log(data["data"])
                    // 创建一个Blob对象，包含SVG内容  
                    const blob = new Blob([data["data"]], { type: 'image/svg+xml;charset=utf-8' });
                    // 创建一个指向该Blob对象的URL  
                    var url = URL.createObjectURL(blob);

                    // 设置隐藏的<a>标签的href属性为该URL  
                    var downloadLink = document.getElementById('downloadLink');
                    downloadLink.href = url;
                    downloadLink.download = name + 'pixelopen-svg.svg'; // 设置下载的文件名  

                    // 触发<a>标签的点击事件以下载文件  
                    downloadLink.click();

                    // 释放URL对象  
                    URL.revokeObjectURL(url);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });
    parentContainer.appendChild(downloadButton);


    // 将父容器添加到 upload-image-btn 中  
    uploadButton.appendChild(parentContainer);

}

// 显示信息函数
function showMessage(msg) {
    var messageContainer = document.getElementById('message-container');
    messageContainer.style.display = 'block'; // 显示容器
    messageContainer.innerHTML = msg
    // 设置3秒后隐藏容器
    setTimeout(function () {
        messageContainer.style.display = 'none';
    }, 3000);
}
// function upload_image() {

//     // 弹窗上传文件    
//     var input = document.createElement("input");
//     input.type = "file";
//     input.accept = "image/*";
//     input.multiple = true; // 允许选择多个文件  
//     input.style.display = 'none'; // 隐藏文件输入    
//     document.body.appendChild(input); // 将输入添加到文档中（尽管它是隐藏的）  

//     input.addEventListener("change", function () {
//         // 获取 upload-image-btn 元素  
//         const uploadButton = document.getElementById('upload-image-btn');

//         // 隐藏 upload-image-btn 下的所有现有子元素（如果有的话）  
//         Array.from(uploadButton.children).forEach(child => {
//             child.style.display = 'none';
//         });

//         var files = input.files;
//         var maxFiles = 6; // 允许的最大文件数量  
//         if (files.length > 0) {
//             var uploadFiles = Array.from(files); // 将 FileList 转换为数组  

//             // 逐个上传文件  
//             uploadFiles.forEach((file, index) => {
//                 if (index < maxFiles) {
//                     if (file.type.startsWith("image/")) {
//                         // 创建 FormData 对象并添加文件  
//                         var formData = new FormData();
//                         formData.append('file', file);
//                         var reader = new FileReader();

//                         // 当文件读取完成时触发的事件处理函数  
//                         reader.onload = function (event) {
//                             // event.target.result 包含文件的 Base64 编码字符串  
//                             var base64String = event.target.result;
//                             // console.log('Base64 string for file ' + file.name + ':', base64String);
//                             addicon(base64String, file.name, index)
//                             // 在这里，您可以将 base64String 发送到服务器，或者用它做其他事情  

//                         };

//                         // 读取文件为 DataURL（即 Base64 编码的字符串）  
//                         reader.readAsDataURL(file);

//                         // 使用 fetch API 发送 POST 请求  
//                         fetch('upload-image/pngtosvg/', {
//                             method: 'POST',
//                             body: formData,
//                             headers: {
//                                 'X-CSRFToken': getCookie('csrftoken')
//                             },
//                         })
//                             .then(response => {
//                                 if (!response.ok) {
//                                     throw new Error('Network response was not ok');
//                                 }
//                                 return response.json();
//                             })
//                             .then(data => {

//                                 document.getElementById(index).style.width = "100%";
//                                 // console.log('Success for file ' + (index + 1) + ':', data["user_png"]);

//                             })
//                             .catch(error => {
//                                 console.error('Error for file ' + (index + 1) + ':', error);
//                             });
//                     }
//                 } else {
//                     console.warn('Skipped non-image file:', file.name);
//                 }
//             });

//             // 移除文件输入元素（可选，如果你不再需要它）  
//             document.body.removeChild(input);
//         } else {
//             alert("No files selected.");
//         }
//     });

//     // 触发文件输入元素的点击事件    
//     input.click();
// }

async function fetchReverseImage2(files) {
    var maxFiles = 8; // 允许的最大文件数量    
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

                // 当文件读取完成时触发的事件处理函数  
                reader.onload = function (event) {
                    // event.target.result 包含文件的 Base64 编码字符串  
                    var base64String = event.target.result;
                    // console.log('Base64 string for file ' + file.name + ':', base64String);
                    addicon(base64String, file.name, i)
                    // 在这里，您可以将 base64String 发送到服务器，或者用它做其他事情  
                    showMessage('图片尺寸有点小，处理时间有点长，请耐心等候~')
                };

                // 读取文件为 DataURL（即 Base64 编码的字符串）  
                reader.readAsDataURL(file);

                try {
                    // 使用 fetch API 发送 POST 请求    
                    const response = await fetch('upload-image/pngtosvg/', {
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

                    document.getElementById('svg' + data['name']).style.width = "100%";
                    document.getElementById('btn' + data['name']).style.opacity = 1;

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

        // 移除文件输入元素（可选，如果你不再需要它）    
        // document.body.removeChild(input);
    } else {
        alert("No files selected.");
    }
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

    // console.log('Success:', data["user_png"]); // 如果需要的话，可以取消注释这行代码
    // console.log(data['is_auth']);
    is_auth = data['is_auth'];
    return data['is_auth']; // 返回解析后的数据中的is_auth字段
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
        // 获取 upload-image-btn 元素    
        const uploadButton = document.getElementById('upload-image-btn');

        // 隐藏 upload-image-btn 下的所有现有子元素（如果有的话）    
        Array.from(uploadButton.children).forEach(child => {
            child.style.display = 'none';
        });

        var files = input.files;
        var maxFiles = 8; // 允许的最大文件数量    
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

                    // 当文件读取完成时触发的事件处理函数  
                    reader.onload = function (event) {
                        // event.target.result 包含文件的 Base64 编码字符串  
                        var base64String = event.target.result;
                        // console.log('Base64 string for file ' + file.name + ':', base64String);
                        addicon(base64String, file.name, i)
                        // 在这里，您可以将 base64String 发送到服务器，或者用它做其他事情  
                        showMessage('图片尺寸有点小，处理时间有点长，请耐心等候~')
                    };

                    // 读取文件为 DataURL（即 Base64 编码的字符串）  
                    reader.readAsDataURL(file);

                    try {
                        // 使用 fetch API 发送 POST 请求    
                        const response = await fetch('upload-image/pngtosvg/', {
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

                        document.getElementById('svg' + data['name']).style.width = "100%";
                        document.getElementById('btn' + data['name']).style.opacity = 1;


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

            // 移除文件输入元素（可选，如果你不再需要它）    
            // document.body.removeChild(input);
        } else {
            alert("No files selected.");
        }
    });

    // 触发文件输入元素的点击事件      
    input.click();
}
