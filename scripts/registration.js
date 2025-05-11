document.getElementById("registration-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    const errorDiv = document.getElementById("error-message");
    const successDiv = document.getElementById("success-message");
    errorDiv.textContent = "";

    const name = document.getElementById("name").value.trim();
    const dob = document.getElementById("birthday").value.trim();
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const repassword = document.getElementById("repassword").value;

    if (!name || !username || !email || !password || !repassword) {
        errorDiv.textContent = "Vui lòng điền đầy đủ tất cả các trường bắt buộc (có dấu *).";
        return;
    }

    const dobPattern = /^(0?[1-9]|[12][0-9]|3[01])[\/](0?[1-9]|1[012])[\/](19|20)\d\d$/;
    if (dob && !dobPattern.test(dob)) {
        errorDiv.textContent = "Ngày sinh không đúng định dạng.";
        return;
    }


    const usernamePattern = /^[a-zA-Z][a-zA-Z0-9_]{3,19}$/;
    if (!usernamePattern.test(username)) {
        errorDiv.textContent = "Tên đăng nhập phải bắt đầu bằng chữ cái, dài 4–20 ký tự, chỉ gồm chữ cái, số, và gạch dưới.";
        return;
    }


    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        errorDiv.textContent = "Email không hợp lệ.";
        return;
    }

    if (password !== repassword) {
        errorDiv.textContent = "Mật khẩu xác nhận không khớp.";
        return;
    }

    try {
        const res = await fetch(`/registration/authorization?username=${encodeURIComponent(username)}&email=${encodeURIComponent(email)}`);
        const data = await res.json();
        if (!data.available) {
            errorDiv.textContent = data.message;
            return;
        }

        const formData = new FormData();
        formData.append("name", name);
        formData.append("dob", dob);
        formData.append("username", username);
        formData.append("email", email);
        formData.append("password", password);

        const resRegister = await fetch("/register", {
            method: "POST",
            body: formData
        });
        const result = await resRegister.json();

        if (resRegister.ok) {
            alert("Đăng ký thành công!");
            window.location.href = "/";
        } else {
            errorDiv.textContent = result.message || "Đăng ký thất bại.";
        }

    } catch (err) {
        errorDiv.textContent = "Có lỗi xảy ra khi kiểm tra dữ liệu hoặc gửi biểu mẫu.";
    }
});
