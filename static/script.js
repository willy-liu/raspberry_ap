function reloadPage() {
    location.reload();
}

function openModal(item) {
    document.getElementById('modal').style.display = 'block';
    document.getElementById('selected-item').innerText = item;
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

// 這個函數會根據勾選框的狀態來顯示或隱藏密碼
function togglePassword() {
    let passwordInput = document.getElementById('password');
    let passwordCheckbox = document.getElementById('show-password');
    console.log("toggle!");
    if (passwordCheckbox.checked) {
        passwordInput.type = 'text';
    } else {
        passwordInput.type = 'password';
    }
}

// 將這個函數綁定到勾選框的改變事件上
document.addEventListener('DOMContentLoaded', function () {
    let showPasswordCheckbox = document.getElementById('show-password');
    if (showPasswordCheckbox) {
        showPasswordCheckbox.addEventListener('change', togglePassword);
    }
});

function submitData() {
    let item = document.getElementById('selected-item').innerText;
    let password = document.getElementById('password').value;

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `item=${item}&password=${password}`
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        closeModal();
        if(data == '1'){
            alert('新增成功！');
        }
        else{
            alert('新增失敗，注意密碼至少要8碼');
        }
        reloadPage();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
