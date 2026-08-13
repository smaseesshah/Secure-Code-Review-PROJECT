import unittest
import requests
import time
import random

# The base URL where your Flask server is running
BASE_URL = 'http://127.0.0.1:3000/api'

class TaskVaultLiveTests(unittest.TestCase):

    def generate_unique_user(self):
        """Generates a random username to avoid database collisions."""
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

    # --- Functional Tests ---

    def test_1_register_and_login(self):
        username, password = self.generate_unique_user()

        res_reg = self.register_user(username, password)
        self.assertEqual(res_reg.status_code, 201)
        self.assertIn('User created successfully', res_reg.json()['message'])

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

        res_create = requests.post(f"{BASE_URL}/tasks", json={"title": "Network Task"}, headers=headers)
        self.assertEqual(res_create.status_code, 201)

        res_get = requests.get(f"{BASE_URL}/tasks", headers=headers)
        self.assertEqual(res_get.status_code, 200)
        tasks = res_get.json()
        
        task_found = any(t['title'] == 'Network Task' and t['owner'] == username for t in tasks)
        self.assertTrue(task_found, "The task we created was not found in the list.")

    def test_3_search_tasks(self):
        username, password = self.generate_unique_user()
        self.register_user(username, password)
        headers = self.get_auth_headers(username)

        unique_title = f"SearchTarget_{username}"
        requests.post(f"{BASE_URL}/tasks", json={"title": unique_title}, headers=headers)

        res_search = requests.get(f"{BASE_URL}/tasks?search={unique_title}", headers=headers)
        self.assertEqual(res_search.status_code, 200)
        
        results = res_search.json()
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]['title'], unique_title)

    def test_4_comments_system(self):
        username, password = self.generate_unique_user()
        self.register_user(username, password)
        headers = self.get_auth_headers(username)

        requests.post(f"{BASE_URL}/tasks", json={"title": "Task for commenting"}, headers=headers)
        
        tasks = requests.get(f"{BASE_URL}/tasks", headers=headers).json()
        my_tasks = [t for t in tasks if t['owner'] == username]
        task_id = my_tasks[-1]['id']

        res_comment = requests.post(f"{BASE_URL}/tasks/{task_id}/comments", 
                                    json={"text": "Live network comment"}, 
                                    headers=headers)
        self.assertEqual(res_comment.status_code, 201)

        res_get_comments = requests.get(f"{BASE_URL}/tasks/{task_id}/comments", headers=headers)
        self.assertEqual(res_get_comments.status_code, 200)
        
        comments = res_get_comments.json()
        comment_found = any(c['username'] == username and c['text'] == 'Live network comment' for c in comments)
        self.assertTrue(comment_found)

    # --- Security Verification Tests ---

    def test_5_security_idor_prevention(self):
        """Verifies that User B cannot delete User A's task (IDOR Fix)"""
        # 1. User A creates a task
        user_a, pass_a = self.generate_unique_user()
        self.register_user(user_a, pass_a)
        headers_a = self.get_auth_headers(user_a)
        requests.post(f"{BASE_URL}/tasks", json={"title": "User A Private Task"}, headers=headers_a)

        tasks = requests.get(f"{BASE_URL}/tasks", headers=headers_a).json()
        task_id = [t['id'] for t in tasks if t['owner'] == user_a][-1]

        # 2. User B registers and tries to delete User A's task
        user_b, pass_b = self.generate_unique_user()
        self.register_user(user_b, pass_b)
        headers_b = self.get_auth_headers(user_b)

        res_del = requests.delete(f"{BASE_URL}/tasks/{task_id}", headers=headers_b)
        
        # 3. Assert that the server blocks it with a 403 Forbidden
        self.assertEqual(res_del.status_code, 403, "IDOR Vulnerability Open: User B successfully deleted User A's task!")

    def test_6_security_sqli_safety(self):
        """Verifies that SQL Injection payloads in search are safely neutralized (SQLi Fix)"""
        username, password = self.generate_unique_user()
        self.register_user(username, password)
        headers = self.get_auth_headers(username)

        # Send a classic SQL injection payload as the search term
        sqli_payload = "' OR '1'='1"
        res_search = requests.get(f"{BASE_URL}/tasks?search={sqli_payload}", headers=headers)
        
        # The app should handle this safely (status 200) and treat the payload as literal text, 
        # returning 0 results instead of dumping the whole database.
        self.assertEqual(res_search.status_code, 200)
        results = res_search.json()
        self.assertEqual(len(results), 0, "SQL Injection Vulnerability Open: Payload altered the query logic!")

if __name__ == '__main__':
    print(f"Running secure verification tests against: {BASE_URL}")
    print("Ensure your Flask server is currently running!")
    unittest.main(verbosity=2)