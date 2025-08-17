let isDragging = false;
let startX, startY, initialScale = 1, activeImg;

let currentScale = 1; // 当前缩放比例  
let startDistance = 0; // 初始触摸点之间的距离  
let offsetX = 0, offsetY = 0; // 图片的偏移量  
let lastX = 0, lastY = 0; // 上一次触摸点的位置  
// let isTouching = false;


document.addEventListener('DOMContentLoaded', function () {
    let isDragging = false;
    let startX, startY, offsetX = 0, offsetY = 0, initialScale = 1;

    const container = document.getElementById('container');
    const images = document.querySelectorAll('.image-wrapper canvas');
    const overlay = document.getElementById('overlay');
    overlay.style.display = 'flex';

    // 获取查询字符串部分（?后面的内容）  
    const queryString = new URLSearchParams(window.location.search);

    // 获取 svg 参数的值  
    const svgValue = queryString.get('svg');

    init_png2svg(svgValue)

    container.addEventListener('mousedown', (e) => {
        isDragging = true;
        startX = e.pageX;
        startY = e.pageY;
        container.style.cursor = 'grabbing';
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
    });

    function onMouseMove(e) {
        if (isDragging) {
            let deltaX = e.pageX - startX;
            let deltaY = e.pageY - startY;

            // 计算新的偏移量  
            let newOffsetX = offsetX + deltaX;
            let newOffsetY = offsetY + deltaY;

            // 获取窗口尺寸和图片尺寸（假设所有图片尺寸相同）  
            const windowWidth = window.innerWidth;
            const windowHeight = window.innerHeight;
            const imgWidth = images[0].clientWidth * initialScale; // 假设所有图片都缩放到相同的比例  
            const imgHeight = images[0].clientHeight * initialScale;

            // 定义拖拽边界（考虑到图片的初始位置和缩放尺寸）  
            const maxLeft = -images[0].getBoundingClientRect().left * initialScale + (windowWidth - imgWidth) / 2; // 允许图片在窗口内左右移动，但不超过边界  
            const maxRight = -images[images.length - 1].getBoundingClientRect().right * initialScale + (windowWidth + imgWidth) / 2; // 考虑到可能有多个图片横向排列  
            const maxTop = -images[0].getBoundingClientRect().top * initialScale + (windowHeight - imgHeight) / 2; // 允许图片在窗口内上下移动，但不超过边界  
            const maxBottom = -images[images.length - 1].getBoundingClientRect().bottom * initialScale + (windowHeight + imgHeight) / 2; // 考虑到可能有多个图片纵向排列  

            // 但是，上面的 maxLeft 和 maxRight 计算可能不准确，因为它们是基于图片的初始位置。  
            // 一个更简单且通常更准确的方法是限制图片的中心点在窗口内。  
            // 因此，我们可以重新计算 maxLeft 和 maxRight，以及 maxTop 和 maxBottom 如下：  

            // 允许图片的中心点在窗口内移动  
            const centerXLimitLeft = -(imgWidth / 2);
            const centerXLimitRight = (imgWidth / 2);
            const centerYLimitTop = -imgHeight;
            const centerYLimitBottom = imgHeight;

            // 应用边缘限制到图片的新偏移量  
            let limitedOffsetX = Math.max(centerXLimitLeft, Math.min(newOffsetX, centerXLimitRight));
            let limitedOffsetY = Math.max(centerYLimitTop, Math.min(newOffsetY, centerYLimitBottom));

            // 更新偏移量  
            offsetX = limitedOffsetX;
            offsetY = limitedOffsetY;

            // 应用偏移量到所有图片上  
            images.forEach(img => {
                img.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${initialScale})`;
            });
            const svgs = document.querySelectorAll('svg');
            svgs.forEach(svgg => {
                const transform = `translate(${offsetX}, ${offsetY}) scale(${initialScale})`;
                svgg.setAttribute('transform', transform);
            });
            // 更新鼠标起始位置为当前位置，为下一次移动做准备（通常不需要这样做，因为我们在每次移动时都重新计算偏移量）  
            // 但为了保持一致性，这里还是更新了 startX 和 startY  
            startX = e.pageX;
            startY = e.pageY;
        }
    }

    function onMouseUp() {
        isDragging = false;
        container.style.cursor = 'grab';
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
    }



    container.addEventListener('wheel', (e) => {
        e.preventDefault();
        let scaleAmount = Math.sign(e.deltaY) * 0.1; // 根据滚轮方向调整缩放比例  
        let newScale = initialScale + scaleAmount;

        // 限制缩放范围（可选）  
        if (newScale > 0.3 && newScale < 3) {
            images.forEach(syncImg => {
                syncImg.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${newScale})`;
            });
            const svgs = document.querySelectorAll('svg');
            svgs.forEach(svgg => {
                const transform = `translate(${offsetX}, ${offsetY}) scale(${newScale})`;
                svgg.setAttribute('transform', transform);
            });
            initialScale = newScale; // 更新初始缩放比例  
        }
    });


    // 点击下载
    document.getElementById('download').addEventListener('click', function () {
        fetch(`/download_svg/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // 如果你的Django项目启用了CSRF保护  
            },
        })
            .then(response => response.json())
            .then(data => {


                // 创建一个Blob对象，包含SVG内容  
                const blob = new Blob([data["data"]], { type: 'image/svg+xml;charset=utf-8' });
                // 创建一个指向该Blob对象的URL  
                var url = URL.createObjectURL(blob);

                // 设置隐藏的<a>标签的href属性为该URL  
                var downloadLink = document.getElementById('downloadLink');
                downloadLink.href = url;
                downloadLink.download = 'pixelopen-svg.svg'; // 设置下载的文件名  

                // 触发<a>标签的点击事件以下载文件  
                downloadLink.click();

                // 释放URL对象  
                URL.revokeObjectURL(url);
            })
            .catch(error => {
                console.error('Error:', error);
            });

    });

    // 点击关闭跳转回主页
    document.getElementById('close-button').addEventListener('click', function () {
        // 把svg文件删除
        fetch(`/delete-file/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // 如果你的Django项目启用了CSRF保护  
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('File deleted successfully!');
                } else {
                    alert('Failed to delete file.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        // 再返回到主页
        window.location.href = '/'
    })


    //禁止右键
    document.addEventListener('contextmenu', function (event) {
        event.preventDefault();
    }, false);

    //重新上传logo
    document.getElementById('uploadlogo').addEventListener('click', function () {
        upload_image()
    })

    //移动端移动
    container.addEventListener('touchstart', (e) => {
        e.preventDefault(); // 阻止默认行为，例如滚动页面  
        isTouching = true;
        const touches = e.touches;
        if (touches.length === 1) {
            // 单点触摸：记录起始位置  
            lastX = touches[0].pageX;
            lastY = touches[0].pageY;
            container.style.cursor = 'move'; // 更改光标样式（在移动端可能无效）  
        } else if (touches.length === 2) {
            // 双点触摸：计算初始距离  
            const touch1 = touches[0];
            const touch2 = touches[1];
            const dx = touch2.pageX - touch1.pageX;
            const dy = touch2.pageY - touch1.pageY;
            startDistance = Math.sqrt(dx * dx + dy * dy);
            var lastScale = currentScale; // 记录上一次缩放比例  
            container.style.cursor = 'grabbing'; // 更改光标样式（在移动端可能无效）  
        }
        document.addEventListener('touchmove', onTouchMove);
        document.addEventListener('touchend', onTouchEnd);
    });

    function onTouchMove(e) {
        // if (!isTouching) return;
        e.preventDefault(); // 阻止默认行为  
        const touches = e.touches;
        if (touches.length === 1) {
            // 单点触摸：计算移动距离并更新偏移量  
            const deltaX = touches[0].pageX - lastX;
            const deltaY = touches[0].pageY - lastY;
            offsetX += deltaX / currentScale;
            offsetY += deltaY / currentScale;
            lastX = touches[0].pageX;
            lastY = touches[0].pageY;

            // 应用偏移量到图片和SVG元素  
            applyTransforms();
        } else if (touches.length === 2) {
            // 双点触摸：计算当前距离并更新缩放比例  
            const touch1 = touches[0];
            const touch2 = touches[1];
            const dx = touch2.pageX - touch1.pageX;
            const dy = touch2.pageY - touch1.pageY;
            const currentDistance = Math.sqrt(dx * dx + dy * dy);
            const scaleChange = currentDistance / startDistance;
            currentScale = lastScale * scaleChange; // 更新当前缩放比例  

            // 限制缩放范围（可选）  
            const minScale = 0.3;
            const maxScale = 3;
            if (currentScale < minScale) currentScale = minScale;
            if (currentScale > maxScale) currentScale = maxScale;

            // 应用缩放比例到图片和SVG元素（同时应用偏移量）  
            applyTransforms();
            // 更新起始距离为当前距离，以便下一次计算缩放比例变化  
            // startDistance = currentDistance;
        }
    }

    function applyTransforms() {
        // 应用缩放和偏移到图片和SVG元素  
        images.forEach(img => {
            img.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${currentScale})`;
        });
        const svgs = document.querySelectorAll('svg');
        svgs.forEach(svgg => {
            svgg.setAttribute('transform', `translate(${offsetX}, ${offsetY}) scale(${currentScale})`);
        });
    }

    function onTouchEnd() {
        // 恢复光标样式（在移动端可能无效）  
        container.style.cursor = '';
        // 如果需要在缩放或移动结束后执行特定操作，可以在这里添加代码  
        // 例如，更新initialScale为currentScale（如果需要在缩放结束后保持缩放比例）  
        initialScale = currentScale; // 根据需求决定是否取消注释  
        lastScale = currentScale;
        // isTouching = false;
        // 移除事件监听器  
        document.removeEventListener('touchmove', onTouchMove);
        document.removeEventListener('touchend', onTouchEnd);
    }

})


function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$&') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : null;
}

function init_png2svg(image_file) {
    fetch('/pngtosvg/', {
        method: 'POST',
        body: JSON.stringify({
            "png_url": image_file
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
        .then(response => response.json())
        .then(data => {
            // console.log('Success:', data);
            document.getElementById('right_image_png').style.display = "none";
            overlay.style.display = 'none';
            // 把svg塞到canvas中

            const svgString = data["svg_content"];

            // 将SVG字符串编码为数据URL  
            const svgDataUrl = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgString);

            // 创建一个Image对象  
            const img = new Image();
            // 设置Image的src为SVG的数据URL  
            img.src = svgDataUrl;

            // 当Image加载完成时，将其绘制到Canvas上  
            img.onload = function () {
                const dpr = window.devicePixelRatio;
                const canvas = document.getElementById('myCanvas');
                canvas.style.width = data["width"];
                canvas.style.height = data["height"];
                canvas.width = data["width"] * 2.5;
                canvas.height = data["height"] * 2.5;
                const ctx = canvas.getContext('2d');
                // ctx.scale(dpr, dpr);
                // 绘制Image到Canvas上  
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            };
        })
        .catch(error => {
            console.error('Error:', error);

        });
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
                fetch('/upload/pngtosvg/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                })
                    .then(response => response.json())
                    .then(data => {
                        let currentUrl = window.location.href;
                        let url = new URL(currentUrl);
                        url.search = '';
                        window.history.replaceState(null, '', url.href);

                        const svgString = data["svg_content"];
                        // 将SVG字符串编码为数据URL  
                        const svgDataUrl = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgString);

                        // 创建一个Image对象  
                        const img = new Image();
                        // 设置Image的src为SVG的数据URL  
                        img.src = svgDataUrl;

                        // 当Image加载完成时，将其绘制到Canvas上  
                        img.onload = function () {
                            const canvas = document.getElementById('myCanvas');
                            canvas.style.width = data["width"];
                            canvas.style.height = data["height"];
                            canvas.width = data["width"] * 2.5;
                            canvas.height = data["height"] * 2.5;
                            const ctx = canvas.getContext('2d');
                            // 绘制Image到Canvas上  
                            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                            document.getElementById('overlay').style.display = 'none';
                        };

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

