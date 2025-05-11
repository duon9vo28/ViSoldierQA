const API_BASE = "http://localhost:8000";
let accessToken = localStorage.getItem("access_token");
let currentConversationId = null;

const centerBox = document.querySelector(".chat-center-box");
const chatHidden = document.querySelector(".chat-hidden");

if (!accessToken) {
    window.location.href = "/";
}

document.addEventListener("DOMContentLoaded", () => {
    loadConversations();

    document.getElementById("message-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const input = document.getElementById("message-input");
        const text = input.value.trim();
        if (!text) return;
        await handleMessageSubmit(text);
        input.value = "";
    });

    document.getElementById("message-form-hidden").addEventListener("submit", async (e) => {
        e.preventDefault();
        const input = document.getElementById("message-input-hidden");
        const text = input.value.trim();
        if (!text) return;
        await handleMessageSubmit(text);
        input.value = "";
    });

    document.getElementById("message-input").addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            document.getElementById("message-form").requestSubmit();
        }
    });

    document.getElementById("message-input-hidden").addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            document.getElementById("message-form-hidden").requestSubmit();
        }
    });
});

function logout() {
    localStorage.removeItem("access_token");
    window.location.href = "/";
}

async function loadConversations() {
    try {
        const res = await fetch(`${API_BASE}/conversations`, {
            headers: { Authorization: `Bearer ${accessToken}` },
        });
        const conversations = await res.json();

        const list = document.getElementById("conversation-list");
        list.innerHTML = "";
        conversations.forEach(conv => {
            const li = document.createElement("li");
            li.className = "chat-item";
            li.innerText = conv.topic || `Hội thoại ${conv.id}`;
            li.title = li.innerText;
            li.addEventListener("click", async () => {
                currentConversationId = conv.id;

                if (centerBox && chatHidden) {
                    centerBox.style.display = "none";
                    chatHidden.style.display = "block";
                }

                await loadMessages(conv.id);
            });
            list.appendChild(li);
        });
    } catch (error) {
        alert("Không thể tải danh sách hội thoại.");
    }
}

async function loadMessages(conversationId) {
    try {
        const res = await fetch(`${API_BASE}/conversations/${conversationId}/messages`, {
            headers: { Authorization: `Bearer ${accessToken}` },
        });
        const messages = await res.json();
        renderMessages(messages);

        document.getElementById("message-input-hidden").disabled = false;
        document.getElementById("message-form-hidden").querySelector("button").disabled = false;
    } catch (error) {
        alert("Không thể tải tin nhắn.");
    }
}

function renderMessages(messages) {
    const chat = document.getElementById("chat-messages");
    chat.innerHTML = "";

    messages.forEach(msg => {
        const messageRow = document.createElement("div");
        messageRow.className = `message-row ${msg.sender}`;

        const avatar = document.createElement("img");
        avatar.className = "avatar";
        avatar.alt = msg.sender;
        avatar.src = msg.sender === "user" ? "/static/images/user_avatar.png" : "/static/images/bot_avatar.jpg";

        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${msg.sender}`;
        messageDiv.innerHTML = marked.parse(msg.message);  // 👈 Markdown render here

        if (msg.sender === "user") {
            messageRow.appendChild(messageDiv);
            messageRow.appendChild(avatar);
        } else {
            messageRow.appendChild(avatar);
            messageRow.appendChild(messageDiv);
        }

        chat.appendChild(messageRow);
    });

    chat.scrollTop = chat.scrollHeight;
}

async function createConversationAndSendMessage(text) {
    try {
        const response = await fetch(`${API_BASE}/conversations`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${accessToken}`,
            },
            body: JSON.stringify({ query: text }),
        });

        const data = await response.json();
        currentConversationId = data.conversation_id;
        await sendMessage(text);
        await loadConversations();
    } catch (error) {
        alert("Không thể tạo cuộc hội thoại mới.");
    }
}

async function sendMessageWithStream(text) {
    const chat = document.getElementById("chat-messages");

    // Hiển thị tin nhắn người dùng
    const userMessageRow = document.createElement("div");
    userMessageRow.className = "message-row user";

    const userAvatar = document.createElement("img");
    userAvatar.className = "avatar";
    userAvatar.alt = "user";
    userAvatar.src = "/static/images/user_avatar.png";

    const userMessageDiv = document.createElement("div");
    userMessageDiv.className = "message user";
    userMessageDiv.textContent = text;

    userMessageRow.appendChild(userMessageDiv);
    userMessageRow.appendChild(userAvatar);
    chat.appendChild(userMessageRow);

    const botMessageRow = document.createElement("div");
    botMessageRow.className = "message-row bot";

    const botAvatar = document.createElement("img");
    botAvatar.className = "avatar";
    botAvatar.alt = "bot";
    botAvatar.src = "/static/images/bot_avatar.jpg";

    const botMessageDiv = document.createElement("div");
    botMessageDiv.className = "message bot";
    botMessageDiv.innerHTML = "";

    botMessageRow.appendChild(botAvatar);
    botMessageRow.appendChild(botMessageDiv);
    chat.appendChild(botMessageRow);

    chat.scrollTop = chat.scrollHeight;

    try {
        const response = await fetch(`${API_BASE}/conversations/${currentConversationId}/messages/stream`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${accessToken}`,
            },
            body: JSON.stringify({ query: text }),
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let done = false;
        let fullResponse = "";

        while (!done) {
            const { value, done: readerDone } = await reader.read();
            done = readerDone;
            const chunk = decoder.decode(value || new Uint8Array(), { stream: !done });
            fullResponse += chunk;
            botMessageDiv.innerHTML = marked.parse(fullResponse);
            chat.scrollTop = chat.scrollHeight;
        }

    } catch (error) {
        botMessageDiv.innerHTML = "<em>[Lỗi]: Không thể nhận phản hồi từ bot.</em>";
    }
}

async function sendMessage(text) {
    await sendMessageWithStream(text);
}

async function handleMessageSubmit(text) {
    if (centerBox && chatHidden) {
        centerBox.style.display = "none";
        chatHidden.style.display = "block";
    }

    if (!currentConversationId) {
        await createConversationAndSendMessage(text);
    } else {
        await sendMessage(text);
    }
}

function goHome() {
    window.location.href = "/chat";
}
