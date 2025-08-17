let R = 0, G = 0, B = 0;
let C = 0, M = 0, Y = 0, K = 0;
let H = 0, S = 0, V = 0;
// 提取CMYK值的正则表达式（不使用命名捕获组）  
let cmykRegexWithoutNames = /CMYK\((\d+)%,\s*(\d+)%,\s*(\d+)%,\s*(\d+)%\)/;

// 提取RGB值的正则表达式（不使用命名捕获组）  
let rgbRegexWithoutNames = /RGB\((\d+),\s*(\d+),\s*(\d+)\)/;

let hsvRegexWithoutNames = /HSV\((\d+),\s*(\d+),\s*(\d+)\)/;

let allcolortype = ["Red", "Blue", "Green", "Cyan", "Magenta", "Yellow", "Black"];


function increaseCounter(buttonElement, inputId, range) {
    var inputElement = document.getElementById(inputId);
    var value = parseInt(inputElement.value, 10);
    if (!isNaN(value) && value < range) {
        inputElement.value = value + 1;
        calculatecolor(inputId, value + 1);
    }




}

function decreaseCounter(buttonElement, inputId, range) {
    var inputElement = document.getElementById(inputId);
    var value = parseInt(inputElement.value, 10);
    if (!isNaN(value) && value > range) {
        inputElement.value = value - 1;
        calculatecolor(inputId, value - 1);
    }



}
function calculatecolor(inputId, value) {
    if (inputId == "Red") {
        R = value;
    }
    if (inputId == "Green") {
        G = value;
    }
    if (inputId == "Blue") {
        B = value;
    }
    if (inputId == "Cyan") {
        C = value;
    }
    if (inputId == "Magenta") {
        M = value;
    }
    if (inputId == "Yellow") {
        Y = value;
    }
    if (inputId == "Black") {
        K = value;
    }

    var rgbelement = document.getElementById('RGB');
    if (rgbelement) {
        rgbelement.value = "RGB(" + R + "," + G + "," + B + ")"
    }

    var cmykelement = document.getElementById('CMYK');
    if (cmykelement) {
        cmykelement.value = "CMYK(" + C + "%," + M + "%," + Y + "%," + K + "%)"
    }

    if (inputId == "Red" || inputId == "Green" || inputId == "Blue") {
        C, M, Y, K = rgbtocmyk(R, G, B)
        H, S, V = rgbtohsv(R, G, B)
    }
    if (inputId == "Cyan" || inputId == "Magenta" || inputId == "Yellow" || inputId == "Black") {
        R, G, B = cmyktorgb(C, M, Y, K)
    }
    cmykelement = document.getElementById('CMYK')
    if (cmykelement) {
        document.getElementById('Cyan').innerHTML = C;
        document.getElementById('Magenta').innerHTML = M;
        document.getElementById('Yellow').innerHTML = Y;
        document.getElementById('Black').innerHTML = K;
    }
}


function limited(inputElement, min, max) {
    inputElement.addEventListener('input', function () {
        // 获取输入的值  
        let value = inputElement.value;
        const inputId = inputElement.id;
        // 尝试将其转换为数字  
        let numberValue = Number(value);

        // 如果转换失败或值大于max，则设置为max  
        if (isNaN(numberValue) || numberValue > max) {
            inputElement.value = max;
        } else if (numberValue < min) { // 通常min为0，但这里为了完整性添加了这个检查  
            inputElement.value = min; // 或者你想要的最小值  
        }
        calculatecolor(inputId, value)
    });
}
function rgbtohsv(R, G, B) {
    H = Math.atan(B / G)
    S = (1 - (3 * Math.min(R, G, B)) / (R + G + B)) * 100
    V = (R + G + B) / 3
    return H, S, V
}

function rgbtocmyk(R, G, B) {
    R1 = R / 255;
    G1 = G / 255;
    B1 = B / 255;


    K = 1 - Math.max(R1, G1, B1);
    C = (1 - R1 - K) / (1 - K)
    C = (1 - G1 - K) / (1 - K)
    C = (1 - B1 - K) / (1 - K)

    C = Math.round(C * 100)
    M = Math.round(M * 100)
    Y = Math.round(Y * 100)
    K = Math.round(K * 100)
    return C, M, Y, K
}

function hsvtorgb(H, S, V) {
    H = H / 60;  // 将角度转换到0-6之间  
    S = S / 100; // 将饱和度转换到0-1之间  
    V = V / 100; // 将亮度转换到0-1之间  

    let I = Math.floor(H);
    let F = H - I;
    let P = V * (1 - S);
    let Q = V * (1 - F * S);
    let T = V * (1 - (1 - F) * S);

    let R, G, B;

    switch (I % 6) {
        case 0: R = V, G = T, B = P; break;
        case 1: R = Q, G = V, B = P; break;
        case 2: R = P, G = V, B = T; break;
        case 3: R = P, G = Q, B = V; break;
        case 4: R = T, G = P, B = V; break;
        case 5: R = V, G = P, B = Q; break;
    }
    R = Math.round(R * 255)
    G = Math.round(G * 255)
    B = Math.round(B * 255)
    return R, G, B
}

function cmyktorgb(C, M, Y, K) {
    C = C / 100; // 将青色转换到0-1之间  
    M = M / 100; // 将洋红色转换到0-1之间  
    Y = Y / 100; // 将黄色转换到0-1之间  
    K = K / 100; // 将黑色（键）转换到0-1之间  

    letR = 255 * (1 - C) * (1 - K);
    G = 255 * (1 - M) * (1 - K);
    B = 255 * (1 - Y) * (1 - K);
    R = Math.round(R)
    G = Math.round(G)
    B = Math.round(B)
    return R, G, B
}
function judgelimited(value, min, max) {
    if (value < min) {
        return min
    }
    else if (value > max) {
        return max
    }
    else {
        return value
    }
}
function updateinput() {
    allcolortype.forEach(function (string) {
        const element = document.getElementById(string);
        if (element) {
            var values = 0
            switch (string) {
                case "Red":
                    values = judgelimited(R, 0, 255);
                    R = values;
                    break;
                case "Green":
                    values = judgelimited(G, 0, 255);
                    G = values;
                    break;
                case "Blue":
                    values = judgelimited(B, 0, 255);
                    B = values;
                    break;
                case "Cyan":
                    values = judgelimited(C, 0, 100);
                    C = values;
                    break;
                case "Magenta":
                    values = judgelimited(M, 0, 100);
                    M = values;
                    break;
                case "Yellow":
                    values = judgelimited(Y, 0, 100);
                    Y = values;
                    break;
                case "Black":
                    values = judgelimited(K, 0, 100);
                    K = values;
                    break;
                default:
                    values = 0;
            }
            element.value = values
        }
    });

}

document.addEventListener('DOMContentLoaded', function () {
    const Red = document.getElementById('Red');
    if (Red) {
        limited(Red, 0, 255)
    }
    const Green = document.getElementById('Green');
    if (Green) {
        limited(Green, 0, 255)
    }
    const Blue = document.getElementById('Blue');
    if (Blue) {
        limited(Blue, 0, 255)
    }

    const Cyan = document.getElementById('Cyan');
    if (Cyan) {
        limited(Cyan, 0, 100)
    }
    const Magenta = document.getElementById('Magenta');
    if (Magenta) {
        limited(Magenta, 0, 100)
    }
    const Yellow = document.getElementById('Yellow');
    if (Yellow) {
        limited(Yellow, 0, 100)
    }
    const Black = document.getElementById('Black');
    if (Black) {
        limited(Black, 0, 100)
    }

    // 获取RGB 
    const RGBElement = document.getElementById('RGB');
    if (RGBElement) {
        // 添加input事件监听器  
        RGBElement.addEventListener('input', function (event) {
            const rgbMatchWithoutNames = event.target.value.match(rgbRegexWithoutNames);
            if (rgbMatchWithoutNames) {
                R = rgbMatchWithoutNames[1];
                G = rgbMatchWithoutNames[2];
                B = rgbMatchWithoutNames[3];
                updateinput();

                var rgbelement = document.getElementById('RGB');
                if (rgbelement) {
                    rgbelement.value = "RGB(" + R + "," + G + "," + B + ")"
                }

                var cmykelement = document.getElementById('CMYK');
                if (cmykelement) {
                    cmykelement.value = "CMYK(" + C + "%," + M + "%," + Y + "%," + K + "%)"
                }
            }

            C, M, Y, K = rgbtocmyk(R, G, B)
            H, S, V = rgbtohsv(R, G, B)
            var cmykelement = document.getElementById('CMYK');
            if (cmykelement) {
                document.getElementById('Cyan').innerHTML = C;
                document.getElementById('Magenta').innerHTML = M;
                document.getElementById('Yellow').innerHTML = Y;
                document.getElementById('Black').innerHTML = K;
            }
        });
    }
    //获取CMYK
    const CMYKElement = document.getElementById('CMYK');
    if (CMYKElement) {
        // 添加input事件监听器  
        CMYKElement.addEventListener('input', function (event) {
            // 解析 cmyk
            const cmykMatchWithoutNames = event.target.value.match(cmykRegexWithoutNames);
            if (cmykMatchWithoutNames) {
                C = cmykMatchWithoutNames[1];
                M = cmykMatchWithoutNames[2];
                Y = cmykMatchWithoutNames[3];
                K = cmykMatchWithoutNames[4];
                updateinput();

                var rgbelement = document.getElementById('RGB');
                if (rgbelement) {
                    rgbelement.value = "RGB(" + R + "," + G + "," + B + ")"
                }

                var cmykelement = document.getElementById('CMYK');
                if (cmykelement) {
                    cmykelement.value = "CMYK(" + C + "%," + M + "%," + Y + "%," + K + "%)"
                }

            }
            R, G, B = cmyktorgb(C, M, Y, K)
            var rgbelement = document.getElementById('RGB');
            if (rgbelement) {
                document.getElementById('Red').innerHTML = R;
                document.getElementById('Green').innerHTML = G;
                document.getElementById('Blue').innerHTML = B;
            }
        });
    }
    document.getElementById('copyButton').addEventListener('click', async () => {
        var rgbelement = document.getElementById('output-Red');
        if (rgbelement) {
            const textToCopy = "RGB(" + R + "," + G + "," + B + ")"
            await navigator.clipboard.writeText(textToCopy);
            alert('copy success!')
        }
        var cmykelement = document.getElementById('output-Cyan');
        if (cmykelement) {
            const textToCopy = "CMYK(" + C + "%," + M + "%," + Y + "%," + K + "%)"
            await navigator.clipboard.writeText(textToCopy);
            alert('copy success!')
        }
    });
})