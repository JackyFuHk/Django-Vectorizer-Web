
// 图片轮播
let timerId = setInterval(() => {
    updateGallery(true)
}, 3000);

function setActive(element) {
    // 移除所有元素的active类  
    document.querySelectorAll('.ok-gallery').forEach(function (el) {
        el.classList.remove('active');
    });

    // 给当前点击的元素添加active类  
    element.classList.add('active');
    // 并且把图片替换到main image里
    document.querySelectorAll('.ok-details-main-image')[0].src = element.src;

}


function updateGallery(next) {
    var galleries = document.querySelectorAll('.ok-gallery');
    var currentIndex = -1;

    // 找到当前激活的索引  
    for (var i = 0; i < galleries.length; i++) {
        if (galleries[i].classList.contains('active')) {
            currentIndex = i;
            break;
        }
    }

    // 移除当前激活的active类  
    if (currentIndex !== -1) {
        galleries[currentIndex].classList.remove('active');
    }

    // 计算下一个或上一个索引  
    var newIndex = (currentIndex + (next ? 1 : -1) + galleries.length) % galleries.length;

    // 给下一个或上一个元素添加active类  
    galleries[newIndex].classList.add('active');
    setActive(galleries[newIndex]);
}


document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('ok-arrow-left').addEventListener('click', function () {
        clearInterval(timerId);
        updateGallery(false); // false 表示是上一个  
    });

    document.getElementById('ok-arrow-right').addEventListener('click', function () {
        clearInterval(timerId);
        updateGallery(true); // true 表示是下一个  
    });
    document.querySelectorAll('.ok-gallery').forEach(function (el) {
        el.addEventListener('click', function () {
            clearInterval(timerId);
        })
    });


    // 图片放大
    const zoomContainer = document.getElementById('zoomContainer');
    const img = document.getElementById('ok-main-image');
    let scale = 1;
    const maxScale = 1.5;

    zoomContainer.addEventListener('mouseenter', function (e) {
        scale = 1;
        zoom(e);
    });

    zoomContainer.addEventListener('mousemove', function (e) {
        zoom(e);
    });

    zoomContainer.addEventListener('mouseleave', function () {
        img.style.transform = 'scale(1)';
        img.style.transformOrigin = 'center center';
    });

    function zoom(e) {
        const rect = zoomContainer.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        if (scale < maxScale) {
            scale += 0.05;
        }

        img.style.transform = `scale(${scale})`;
        img.style.transformOrigin = `${x / scale}px ${y / scale}px`;
    }

    // 点击表格选中。
    var tableRows = document.querySelectorAll('.ok-details-tiered-price-table tbody tr');

    tableRows.forEach(function (row) {
        row.addEventListener('click', function () {
            // 移除其他行的selected类  
            tableRows.forEach(function (otherRow) {
                otherRow.classList.remove('selected');
            });

            // 给当前行添加selected类  
            this.classList.add('selected');

            // 更新总价
            var quantity = this.querySelector('td:first-child').textContent;
            var pcsprice = this.querySelector('td:last-child').textContent;
            document.getElementById('ok-total-price').innerHTML = "&#163;" + (quantity * pcsprice).toFixed(2);

            // 更新save多少
            var tables = document.querySelectorAll('.ok-details-tiered-price-table');

            tables.forEach(function (table) {
                // 使用getComputedStyle来获取表格的最终显示状态  
                var displayStyle = window.getComputedStyle(table).display;

                // 检查表格是否可见（即不是none）  
                if (displayStyle !== 'none') {
                    var firstRow = table.querySelector('tbody tr:first-child');

                    if (firstRow) {
                        var firstprice = firstRow.querySelector(':last-child').textContent;

                        // 将文本内容转换为数字（注意：这里假设文本内容是有效的数字）  
                        firstprice = parseFloat(firstprice.replace(/[^0-9\.]/g, ''));

                        // 计算节省的百分比  
                        var savePercentage = Math.round(100 * (pcsprice - firstprice) / firstprice);

                        // 同样地，假设所有你想要更新的元素都有类名 "ok-total-price"  
                        var elements = document.querySelectorAll('#ok-save-money');

                        // 使用 forEach 遍历所有元素并更新它们的 innerHTML  
                        elements.forEach(function (element) {
                            element.innerHTML = savePercentage + "%"; // 将每个元素的 innerHTML 设置为 "新的内容"  
                        });

                    }
                }
            });

        });
    });

    // 点击variation转换table
    var variationSizes = document.querySelectorAll('.ok-variation-size');

    variationSizes.forEach(function (size) {
        size.addEventListener('click', function () {
            // 获取关联的表格ID  
            var variationName = this.getAttribute('data-variation-name');
            var tableId = 'price-table-' + variationName;

            // 隐藏所有表格  
            var tables = document.querySelectorAll('.ok-details-tiered-price-table');
            tables.forEach(function (table) {
                table.style.display = 'none';
            });

            // 显示对应的表格  
            var targetTable = document.getElementById(tableId);
            if (targetTable) {
                targetTable.style.display = 'table'; // 或者使用 'block'，但'table'是更具体的值  
            }

            // 获取所有.ok-details-tiered-price-table表格  
            document.querySelectorAll('.ok-details-tiered-price-table tbody tr.selected').forEach(function (row) {
                row.classList.remove('selected');
            });
            var tables = document.querySelectorAll('.ok-details-tiered-price-table');

            tables.forEach(function (table) {

                // 使用getComputedStyle获取表格的display样式  
                var displayStyle = window.getComputedStyle(table).display;

                // 检查display样式是否为block（或其他非none的值，但这里我们假设如果是通过JS显示的，则会是block）  
                if (displayStyle !== 'none') {
                    // 获取第一个<tr>元素并添加selected类  
                    var firstRow = table.querySelector('tbody tr');
                    if (firstRow) {
                        firstRow.classList.add('selected');
                    }

                    // 同样地，假设所有你想要更新的元素都有类名 "ok-total-price"  
                    var elements = document.querySelectorAll('#ok-save-money');

                    // 使用 forEach 遍历所有元素并更新它们的 innerHTML  
                    elements.forEach(function (element) {
                        element.innerHTML = "0%"; // 将每个元素的 innerHTML 设置为 "新的内容"  
                    });
                }
            });


        });
    });



    //默认初始化价格  
    var table = document.querySelector('.ok-details-tiered-price-table');
    var firstRow = table.querySelector('tbody tr:first-child');

    if (firstRow) {
        var quantity = firstRow.querySelector(':first-child').textContent;
        var pcsprice = firstRow.querySelector(':last-child').textContent;

        document.getElementById('ok-total-price').innerHTML = "&#163;" + quantity * pcsprice;

    } else {
        console.log('No first row found in the table.');
    }

    //倒计时

    // 初始调用一次以立即显示初始倒计时和日期  
    updateCountdown();

    // 每秒更新一次  
    var countdownTimer = setInterval(updateCountdown, 1000);

})


function updateCountdown() {
    // 获取当前时间  
    var now = new Date();

    // 计算两个月后的日期  
    var twoMonthsLater = new Date(now);
    twoMonthsLater.setMonth(now.getMonth() + 2);

    // 格式化日期字符串（假设您想要YYYY-MM-DD格式）  
    var expiryDateString = ('0' + twoMonthsLater.getDate()).slice(-2) + '/' +
        ('0' + (twoMonthsLater.getMonth() + 1)).slice(-2) + '/' +
        twoMonthsLater.getFullYear();

    // 设置“Got this by”的日期  
    document.getElementById("expiryDate").innerText = expiryDateString;

    // 计算距离次日00:00的时间差（为了示例简单，这里仍使用次日00:00，但您可以根据需要调整）  
    // 注意：这里应该根据您的实际需求来计算截止时间  
    var targetDate = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);
    targetDate.setHours(0, 0, 0, 0);

    var distance = targetDate - now;

    // 时间计算  
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // 显示时间  
    document.getElementById("hours").innerText = hours.toString().padStart(2, '0');
    document.getElementById("minutes").innerText = minutes.toString().padStart(2, '0');
    document.getElementById("seconds").innerText = seconds.toString().padStart(2, '0');

    // 如果倒计时结束，停止更新  
    if (distance < 0) {
        updateCountdown();
    }
}

