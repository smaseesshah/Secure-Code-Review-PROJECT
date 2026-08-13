// Base URL for the local Flask backend
const API_URL = '/api';

// --- Utility Functions ---

function showMessage(msg, isError = false) {
    const msgBox = document.getElementById('messageBox');
    if (msgBox) {
        msgBox.textContent = msg;
        msgBox.style.color = isError ? 'red' : 'green';
    }
}

function getAuthHeaders() {
    const user = localStorage.getItem('currentUser');
    return {
        'Content-Type': 'application/json',
        'Authorization': user ? `Bearer ${user}` : ''
    };
}

function logout() {
    localStorage.removeItem('currentUser');
    window.location.href = '/login.html';
}

// --- Auth Logic ---

const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch(`${API_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();
            
            if (response.ok) {
                showMessage('Registration successful! Please login.');
                setTimeout(() => window.location.href = '/login.html', 1500);
            } else {
                showMessage(data.error, true);
            }
        } catch (err) {
            showMessage('Connection error', true);
        }
    });
}

const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();
            
            if (response.ok) {
                localStorage.setItem('currentUser', username);
                window.location.href = '/dashboard.html';
            } else {
                showMessage(data.error, true);
            }
        } catch (err) {
            showMessage('Connection error', true);
        }
    });
}

// --- Dashboard Logic ---

const createTaskForm = document.getElementById('createTaskForm');
if (createTaskForm) {
    createTaskForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('taskTitle').value;

        await fetch(`${API_URL}/tasks`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ title })
        });
        
        document.getElementById('taskTitle').value = '';
        
        // Instantly reload tasks so user sees the new one
        loadTasks(); 
    });
}

async function loadTasks(searchQuery = '') {

    if (typeof searchQuery !== 'string') {
        searchQuery = '';
    }

    const myTaskList = document.getElementById('myTaskList');
    const otherTaskList = document.getElementById('otherTaskList');
    
    if (!myTaskList || !otherTaskList) return;

    let url = `${API_URL}/tasks`;
    if (searchQuery) {
        url += `?search=${encodeURIComponent(searchQuery)}`;
    }

    try {
        const response = await fetch(url, { headers: getAuthHeaders() });
        
        if (response.status === 401) {
            logout();
            return;
        }

        const tasks = await response.json();
        const currentUser = localStorage.getItem('currentUser');

        // Clear both lists instantly before injecting new data
        myTaskList.innerHTML = '';
        otherTaskList.innerHTML = '';

        tasks.forEach(task => {
            const li = document.createElement('li');
            li.className = 'task-item';
            
            // Only generate a delete button if it's YOUR task (IDOR target)
            let deleteButtonHTML = '';
            if (task.owner === currentUser) {
                deleteButtonHTML = `<button onclick="deleteTask(${task.id})" class="btn-danger">Delete</button>`;
            }
            
            li.innerHTML = `
                <a href="/task.html?id=${task.id}" class="task-title">${he.encode(task.title)}</a>
                ${deleteButtonHTML}
            `;

            // INJECT DYNAMICALLY: Check owner and put in the correct box
            if (task.owner === currentUser) {
                myTaskList.appendChild(li);
            } else {
                // For other tasks, it helps to see who created it
                li.innerHTML = `<a href="/task.html?id=${task.id}" class="task-title">${he.encode(task.title)} <span style="font-size: 0.8em; color: gray;">(by ${task.owner})</span></a>`;
                otherTaskList.appendChild(li);
            }
        });
    } catch (err) {
        console.error("Failed to load tasks:", err);
    }
}

function searchTasks() {
    const query = document.getElementById('searchInput').value;
    loadTasks(query);
}

async function deleteTask(taskId) {
    await fetch(`${API_URL}/tasks/${taskId}`, {
        method: 'DELETE',
        headers: getAuthHeaders()
    });
    loadTasks(); 
}

// --- Task Details & Comments Logic ---

async function loadTaskDetails(taskId) {
    if (!taskId) return;
    
    document.getElementById('currentTaskId').value = taskId;

    const taskRes = await fetch(`${API_URL}/tasks/${taskId}`, { headers: getAuthHeaders() });
    const task = await taskRes.json();
    document.getElementById('taskTitleDisplay').textContent = task.title;

    const commentRes = await fetch(`${API_URL}/tasks/${taskId}/comments`, { headers: getAuthHeaders() });
    const comments = await commentRes.json();
    displayComments(comments);
}

function displayComments(comments) {
    const container = document.getElementById('commentsList');
    container.innerHTML = '';

    comments.forEach(c => {
        const div = document.createElement('div');
        div.className = 'comment-box';
        
        // VULNERABLE LINE: Target for Stored XSS
        //div.innerHTML = `<strong>${c.username}:</strong> ${c.text}`;


        // FIX Code

        // Level 1 : Encoding the inputs using he libary
        const safeUname = he.encode(c.username);
        const safeText = he.encode(c.text);

        // Level 2 : Using safe HTML tags
        const strong = document.createElement('strong');
        strong.textContent = `${safeUname}: `;
        div.append(strong,safeText);


        container.appendChild(div);
    });
}

const commentForm = document.getElementById('commentForm');
if (commentForm) {
    commentForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const taskId = document.getElementById('currentTaskId').value;
        const text = document.getElementById('commentText').value;

        await fetch(`${API_URL}/tasks/${taskId}/comments`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ text })
        });

        document.getElementById('commentText').value = '';
        loadTaskDetails(taskId); 
    });
}

// ==========================================
// INITIALIZATION ON PAGE LOAD
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    
    const myTaskListElement = document.getElementById('myTaskList');
    
    if (myTaskListElement) {
        loadTasks();

        setInterval(() => {
            const searchInput = document.getElementById('searchInput');
            if (searchInput && searchInput.value === '') {
                loadTasks();
            }
        }, 60000); 
    }

    const urlParams = new URLSearchParams(window.location.search);
    const taskId = urlParams.get('id');
    if (taskId) {
        loadTaskDetails(taskId);
    }
});