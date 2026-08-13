import unittest
import requests
import time
import random

# The base URL where your Flask server is actually running
BASE_URL = 'http://127.0.0.1:3000/api'

class TaskVaultLiveTests(unittest.TestCase):

    def generate_unique_user(self):
        """Generates a random username to avoid database collisions on repeated test runs."""
        random_suffix = random.randint(1000, 9999)
        return f"testuser_{int(time.time())}_{random_suffix}", "password123"

    def register_user(self, username, password):
        """Helper to register a user over the network."""
        return requests.post(f"{BASE_URL}/register", json={
            "username": username,
            "password": password
        })

    def get_auth_headers(self, username):
        """Helper to generate the authentication header."""
        return {"Content-Type": "application/json", "Authorization": f"Bearer {username}"}

    # --- Test Cases ---

    def test_1_register_and_login(self):
        username, password = self.generate_unique_user()

        # 1. Register User
        res_reg = self.register_user(username, password)
        self.assertEqual(res_reg.status_code, 201)
        self.assertIn('User created successfully', res_reg.json()['message'])

        # 2. Login User
        res_login = requests.post(f"{BASE_URL}/login", json={
            "username": username,
            "password": password
        })
        self.assertEqual(res_login.status_code, 200)
        self.assertIn('Login successful', res_login.json()['message'])

    def test_2_create_and_get_tasks(self):
        username, password = self.generate_unique_user()
        self.register_user(username, password)
        headers = self.get_auth_headers(username)

        # 1. Create a task
        res_create = requests.post(f"{BASE_URL}/tasks", json={"title": "Network Task"}, headers=headers)
        self.assertEqual(res_create.status_code, 201)

        # 2. Get all tasks
        res_get = requests.get(f"{BASE_URL}/tasks", headers=headers)
        self.assertEqual(res_get.status_code, 200)
        tasks = res_get.json()
        
        # Make sure our created task is in the response
        task_found = any(t['title'] == 'Network Task' and t['owner'] == username for t in tasks)
        self.assertTrue(task_found, "The task we created was not found in the list.")

    def test_3_search_tasks(self):
        username, password = self.generate_unique_user()
        self.register_user(username, password)
        headers = self.get_auth_headers(username)

        # Create a task with a highly unique name
        unique_title = f"SearchTarget_{username}"
        requests.post(f"{BASE_URL}/tasks", json={"title": unique_title}, headers=headers)

        # Search for that specific task
        res_search = requests.get(f"{BASE_URL}/tasks?search={unique_title}", headers=headers)
        self.assertEqual(res_search.status_code, 200)
        
        results = res_search.json()
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]['title'], unique_title)

    def test_4_comments_system(self):
        username, password = self.generate_unique_user()
        self.register_user(username, password)
        headers = self.get_auth_headers(username)

        # Create a task
        requests.post(f"{BASE_URL}/tasks", json={"title": "Task for commenting"}, headers=headers)
        
        # Get the task ID. (It will be the last task created by this user)
        tasks = requests.get(f"{BASE_URL}/tasks", headers=headers).json()
        my_tasks = [t for t in tasks if t['owner'] == username]
        task_id = my_tasks[-1]['id']

        # Add a comment
        res_comment = requests.post(f"{BASE_URL}/tasks/{task_id}/comments", 
                                    json={"text": "Live network comment"}, 
                                    headers=headers)
        self.assertEqual(res_comment.status_code, 201)

        # Retrieve comments
        res_get_comments = requests.get(f"{BASE_URL}/tasks/{task_id}/comments", headers=headers)
        self.assertEqual(res_get_comments.status_code, 200)
        
        comments = res_get_comments.json()
        comment_found = any(c['username'] == username and c['text'] == 'Live network comment' for c in comments)
        self.assertTrue(comment_found)

    def test_5_delete_task(self):
        username, password = self.generate_unique_user()
        self.register_user(username, password)
        headers = self.get_auth_headers(username)

        # Create a task
        requests.post(f"{BASE_URL}/tasks", json={"title": "Delete me!"}, headers=headers)
        
        # Get the task ID
        tasks = requests.get(f"{BASE_URL}/tasks", headers=headers).json()
        my_tasks = [t for t in tasks if t['owner'] == username]
        task_id = my_tasks[-1]['id']

        # Delete it
        res_del = requests.delete(f"{BASE_URL}/tasks/{task_id}", headers=headers)
        self.assertEqual(res_del.status_code, 200)

        # Verify it returns a 404 Not Found
        res_verify = requests.get(f"{BASE_URL}/tasks/{task_id}", headers=headers)
        self.assertEqual(res_verify.status_code, 404)

if __name__ == '__main__':
    print(f"Running tests against: {BASE_URL}")
    print("Ensure your Flask server is currently running!")
    unittest.main(verbosity=2)