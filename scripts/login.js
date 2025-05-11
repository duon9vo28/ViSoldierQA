document.addEventListener("DOMContentLoaded", () => {

    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");
    const form = document.getElementById("loginForm");

    const token = localStorage.getItem("access_token");
    if (token) {
        window.location.href = "/chat";
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new URLSearchParams();
        formData.append("username", usernameInput.value);
        formData.append("password", passwordInput.value);

        const errorDisplay = document.getElementById("errorMessage");
        errorDisplay.textContent = ""; // reset error

        try {
            const response = await fetch("http://localhost:8000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: formData.toString()
            });

            const data = await response.json();

            if (data.success == "True") {
                localStorage.setItem("access_token", data.access_token);
                window.location.href = "/chat";
            } else {
                errorDisplay.textContent = data.message || "Đăng nhập thất bại.";
            }
        } catch (error) {
            errorDisplay.textContent = "Không thể kết nối tới server!";
        }
    });
});
