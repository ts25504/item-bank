import unittest
import json
from flask import url_for
from app import create_app, db
from app.model.point_model import Points
from app.model.subject_model import Subject


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        Subject.generate_fake(1)
        Points.generate_fake(10)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_single_choice(self):
        response = self.client.get(
            url_for('api.get_single_choices'),
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 200)

        response = self.client.post(
            url_for('api.new_single_choice'),
            headers=self.get_api_headers(),
            data=json.dumps({
                'question': 'test question',
                'difficult_level': 0.5,
                'faq': 'test faq',
                'subject': 1,
                'points': 1,
                'answer': 'A',
                'A': 'test A',
                'B': 'test B',
                'C': 'test C',
                'D': 'test D'
            }))
        self.assertTrue(response.status_code == 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        response = self.client.get(
            url,
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['question'] == 'test question')
        self.assertTrue(json_response['difficult_level'] == 0.5)
        self.assertTrue(json_response['faq'] == 'test faq')
        self.assertTrue(json_response['answer'] == 'A')
        self.assertTrue(json_response['A'] == 'test A')
        self.assertTrue(json_response['B'] == 'test B')
        self.assertTrue(json_response['C'] == 'test C')
        self.assertTrue(json_response['D'] == 'test D')
        self.assertTrue(json_response['subject'] == 1)
        self.assertTrue(json_response['points'] == 1)
        id = json_response['id']

        response = self.client.put(
            url,
            headers=self.get_api_headers(),
            data=json.dumps({
                'question': 'modified question',
                'answer': 'B'
            }))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['question'] == 'modified question')
        self.assertTrue(json_response['answer'] == 'B')

        response = self.client.delete(
            url_for('api.delete_single_choice', id=id, _external=True),
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 204)

        response = self.client.get(
            url,
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 404)

    def test_blank_fill(self):
        response = self.client.get(
            url_for('api.get_blank_fills'),
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 200)

        response = self.client.post(
            url_for('api.new_blank_fill'),
            headers=self.get_api_headers(),
            data=json.dumps({
                'question': 'test question',
                'difficult_level': 0.5,
                'faq': 'test faq',
                'subject': 1,
                'points': 1,
                'answer': 'test answer'
            }))
        self.assertTrue(response.status_code == 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        response = self.client.get(
            url,
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['question'] == 'test question')
        self.assertTrue(json_response['difficult_level'] == 0.5)
        self.assertTrue(json_response['faq'] == 'test faq')
        self.assertTrue(json_response['answer'] == 'test answer')
        self.assertTrue(json_response['subject'] == 1)
        self.assertTrue(json_response['points'] == 1)
        id = json_response['id']

        response = self.client.put(
            url,
            headers=self.get_api_headers(),
            data=json.dumps({
                'question': 'modified question',
                'answer': 'modified answer'
            }))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['question'] == 'modified question')
        self.assertTrue(json_response['answer'] == 'modified answer')

        response = self.client.delete(
            url_for('api.delete_blank_fill', id=id, _external=True),
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 204)

        response = self.client.get(
            url,
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 404)

    def test_essay(self):
        response = self.client.get(
            url_for('api.get_essays'),
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 200)

        response = self.client.post(
            url_for('api.new_essay'),
            headers=self.get_api_headers(),
            data=json.dumps({
                'question': 'test question',
                'difficult_level': 0.5,
                'faq': 'test faq',
                'subject': 1,
                'points': 1,
                'answer': 'test answer'
            }))
        self.assertTrue(response.status_code == 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        response = self.client.get(
            url,
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['question'] == 'test question')
        self.assertTrue(json_response['difficult_level'] == 0.5)
        self.assertTrue(json_response['faq'] == 'test faq')
        self.assertTrue(json_response['answer'] == 'test answer')
        self.assertTrue(json_response['subject'] == 1)
        self.assertTrue(json_response['points'] == 1)
        id = json_response['id']

        response = self.client.put(
            url,
            headers=self.get_api_headers(),
            data=json.dumps({
                'question': 'modified question',
                'answer': 'modified answer'
            }))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['question'] == 'modified question')
        self.assertTrue(json_response['answer'] == 'modified answer')

        response = self.client.delete(
            url_for('api.delete_essay', id=id, _external=True),
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 204)

        response = self.client.get(
            url,
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 404)

    def test_points(self):
        response = self.client.get(
            url_for('api.get_points'),
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 200)

        response = self.client.post(
            url_for('api.new_point'),
            headers=self.get_api_headers(),
            data=json.dumps({
                'name': 'test name',
                'subject': 1
            }))
        self.assertTrue(response.status_code == 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        response = self.client.get(
            url,
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['name'] == 'test name')
        self.assertTrue(json_response['subject'] == 1)
        id = json_response['id']

        response = self.client.put(
            url,
            headers=self.get_api_headers(),
            data=json.dumps({'name': 'modified name'}))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['name'] == 'modified name')

        response = self.client.delete(
            url_for('api.delete_point', id=id, _external=True),
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 204)

        response = self.client.get(
            url,
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 404)

    def test_subject(self):
        response = self.client.get(
            url_for('api.get_subjects'),
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 200)

        response = self.client.post(
            url_for('api.new_subject'),
            headers=self.get_api_headers(),
            data=json.dumps({'name': 'test name'}))
        self.assertTrue(response.status_code == 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        response = self.client.get(
            url,
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['name'] == 'test name')
        id = json_response['id']

        response = self.client.put(
            url,
            headers=self.get_api_headers(),
            data=json.dumps({'name': 'modified name'}))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['name'] == 'modified name')

        response = self.client.delete(
            url_for('api.delete_subject', id=id, _external=True),
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 204)

        response = self.client.get(
            url,
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 404)
