
let rowData = {};
document.addEventListener('DOMContentLoaded', function () {

    var language = getCookie("language");
    if (language == 'english') {
        hide_price("webapp-pricing-table", "RMB")
        hide_price("api-pricing-table", "RMB")
        document.getElementById('alipay-btn').style.display = 'none';
    }
    if (language == 'chinese') {
        hide_price("webapp-pricing-table", "USD")
        hide_price("api-pricing-table", "USD")
        document.getElementById('paypal-btn').style.display = 'none';
    }
    const firstTable = document.getElementById("webapp-pricing-table"); // 假设你要操作的是第一个表格  
    const firstRow = firstTable.querySelector('tr:not(:first-child)'); // 跳过可能的表头行  

    if (firstRow) {
        // 将第一行的背景颜色设置为橙色  
        firstRow.style.backgroundColor = 'orange';
    } else {
        console.warn('No data rows found in the first table.');
    }
    // 定义一个函数来处理行点击事件  
    function handleRowClick(event, tableid) {
        // 存储表头的引用，以便在点击事件中使用  
        const tableHeaders = [];

        // 获取表格和表头  
        const table = document.getElementById(tableid); // 替换为你的表格ID  
        if (!table) {
            console.error('Table not found');
            return;
        }

        // 获取表头行  
        const headerRow = table.querySelector('tr:first-child');
        if (!headerRow) {
            console.warn('No header row found in the table.');
            return;
        }

        // 获取表头单元格并存储其文本内容  
        const headerCells = headerRow.querySelectorAll('th');
        if (headerCells.length === 0) {
            console.warn('No header cells found in the header row.');
            return;
        }
        headerCells.forEach(headerCell => {
            tableHeaders.push(headerCell.textContent.trim());
        });
        // 移除所有表格中行的橙色背景（如果有的话）  
        const allRows = document.querySelectorAll('table tr');
        allRows.forEach(row => {
            row.style.backgroundColor = '';
        });

        // 获取被点击的行  
        const clickedRow = event.target.parentElement; // event.target 可能是单元格，所以取其父元素（行）  

        // 将被点击的行的背景颜色设置为橙色  
        clickedRow.style.backgroundColor = 'orange';

        // 获取被点击行的所有单元格的值  

        const rowCells = clickedRow.querySelectorAll('td');
        rowCells.forEach((cell, index) => {
            rowData[tableHeaders[index]] = cell.textContent.trim();
        });

        if (tableid == "webapp-pricing-table") {
            rowData["Mode"] = "webapp";
        }
        if (tableid == "api-pricing-table") {
            rowData["Mode"] = "api";
        }


    }

    // 为第一个表格的所有行添加点击事件监听器  
    document.getElementById("webapp-pricing-table").addEventListener('click', function (event) {
        if (event.target.tagName.toLowerCase() === 'td') { // 确保点击的是单元格  
            handleRowClick(event, "webapp-pricing-table");
        }
    });

    // 为第二个表格的所有行添加点击事件监听器（同样处理）  
    document.getElementById("api-pricing-table").addEventListener('click', function (event) {
        if (event.target.tagName.toLowerCase() === 'td') { // 确保点击的是单元格  
            handleRowClick(event, "api-pricing-table");
        }
    });
    document.getElementById('alipay-btn').addEventListener('click', function () {
        console.log(rowData)
        if (rowData['Mode'] == 'api') {
            requestbody = {
                mode: rowData['Mode'],
                currency: rowData['Currency'],
                price: rowData['Price'],
                period: rowData['Credits']
            }
        }
        if (rowData['Mode'] == 'webapp') {
            requestbody = {
                mode: rowData['Mode'],
                currency: rowData['Currency'],
                price: rowData['Price'],
                period: rowData['Month']
            }
        }
        fetch(`/payment/paypal/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // 如果你的Django项目启用了CSRF保护  
            },
            body: requestbody
        })
            .then(response => response.json())
            .then(data => {

            })
            .catch(error => {
                console.error('Error:', error);
            });

    });

})
document.getElementById('paypal-btn').addEventListener('click', function () {
    console.log(rowData)
    if (rowData['Mode'] == 'api') {
        requestbody = {
            mode: rowData['Mode'],
            currency: rowData['Currency'],
            price: rowData['Price'],
            period: rowData['Credits']
        }
    }
    if (rowData['Mode'] == 'webapp') {
        requestbody = {
            mode: rowData['Mode'],
            currency: rowData['Currency'],
            price: rowData['Price'],
            period: rowData['Month']
        }
    }
    fetch(`/payment/alipay/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // 如果你的Django项目启用了CSRF保护  
        },
        body: requestbody
    })
        .then(response => response.json())
        .then(data => {

        })
        .catch(error => {
            console.error('Error:', error);
        });

});


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

function hide_price(id, innertext) {
    // 获取表格元素  
    var table = document.getElementById(id);

    // 获取表格的所有行（不包括表头）  
    var rows = table.getElementsByTagName('tr');

    // 遍历所有行（从1开始，因为0是表头）  
    for (var i = 1; i < rows.length; i++) {
        // 获取当前行的所有单元格  
        var cells = rows[i].getElementsByTagName('td');

        // 假设Status是第三列（索引为2，因为索引从0开始）  
        var statusCell = cells[0];

        // 获取Status单元格的文本内容  
        var status = statusCell.textContent || statusCell.innerText; // 兼容性处理  

        // 检查Status是否为"Inactive"  
        if (status === innertext) {
            // 如果是，则隐藏整行  
            rows[i].style.display = 'none';
        }
    }
}