import random
from flask.ext.testing import TestCase
import pytest

import ara.webapp as w
import ara.models as m

from common import ansible_run


class TestApp(TestCase):
    '''Tests for the ARA web interface'''

    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True

    def create_app(self):
        return w.create_app(self)

    def setUp(self):
        m.db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        m.db.session.remove()
        m.db.drop_all()

    def test_overview(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)

    def test_list_playbook(self):
        ansible_run()
        res = self.client.get('/playbook/')
        self.assertEqual(res.status_code, 200)

    def test_list_playbook_incomplete(self):
        ansible_run(complete=False)
        res = self.client.get('/playbook/')
        self.assertEqual(res.status_code, 200)

    def test_show_playbook(self):
        ctx = ansible_run()
        res = self.client.get('/playbook/{}/'.format(
            ctx['playbook'].id))
        self.assertEqual(res.status_code, 200)

    def test_show_playbook_missing(self):
        ansible_run()
        res = self.client.get('/playbook/foo/')
        self.assertEqual(res.status_code, 404)

    @pytest.mark.incomplete
    def test_show_playbook_incomplete(self):
        ctx = ansible_run(complete=False)
        res = self.client.get('/playbook/{}/'.format(
            ctx['playbook'].id))
        self.assertEqual(res.status_code, 200)

    def test_show_playbook_results(self):
        ctx = ansible_run()
        res = self.client.get('/playbook/{}/results/'.format(
            ctx['playbook'].id))
        self.assertEqual(res.status_code, 200)

    def test_show_playbook_results_host(self):
        ctx = ansible_run()
        res = self.client.get('/playbook/{}/host/{}/'.format(
            ctx['playbook'].id,
            ctx['host'].name))
        self.assertEqual(res.status_code, 200)

    def test_show_playbook_results_host_status(self):
        ctx = ansible_run()
        res = self.client.get('/playbook/{}/host/{}/ok/'.format(
            ctx['playbook'].id,
            ctx['host'].name))
        self.assertEqual(res.status_code, 200)

    def test_show_playbook_results_play(self):
        ctx = ansible_run()
        res = self.client.get('/playbook/{}/play/{}/'.format(
            ctx['playbook'].id,
            ctx['play'].id))
        self.assertEqual(res.status_code, 200)

    def test_show_playbook_results_task(self):
        ctx = ansible_run()
        res = self.client.get('/playbook/{}/task/{}/'.format(
            ctx['playbook'].id,
            ctx['task'].id))
        self.assertEqual(res.status_code, 200)

    def test_show_playbook_results_missing(self):
        ansible_run()
        res = self.client.get('/playbook/foo/results/')
        self.assertEqual(res.status_code, 404)

    def test_show_host(self):
        ctx = ansible_run()
        res = self.client.get('/host/{}/'.format(ctx['host'].id))
        self.assertEqual(res.status_code, 200)

    def test_show_host_missing(self):
        ansible_run()
        res = self.client.get('/host/foo/')
        self.assertEqual(res.status_code, 404)

    def test_show_host_exists_facts_missing(self):
        ctx = ansible_run(gather_facts=False)
        res = self.client.get('/host/{}/'.format(ctx['host'].id))
        self.assertEqual(res.status_code, 404)

    def test_show_host_missing_facts_missing(self):
        ansible_run()
        res = self.client.get('/host/foo/')
        self.assertEqual(res.status_code, 404)

    @pytest.mark.incomplete
    def test_show_host_incomplete(self):
        ctx = ansible_run(complete=False)
        res = self.client.get('/host/{}/'.format(ctx['host'].id))
        self.assertEqual(res.status_code, 200)

    def test_show_result(self):
        ctx = ansible_run()
        res = self.client.get('/result/{}/'.format(
            ctx['result'].id))
        self.assertEqual(res.status_code, 200)

    def test_show_result_missing(self):
        ansible_run()
        res = self.client.get('/result/foo/')
        self.assertEqual(res.status_code, 404)

    @pytest.mark.incomplete
    def test_show_result_incomplete(self):
        ctx = ansible_run(complete=False)
        res = self.client.get('/result/{}/'.format(
            ctx['result'].id))
        self.assertEqual(res.status_code, 200)
