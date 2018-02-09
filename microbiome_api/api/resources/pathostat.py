import random
import time
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from microbiome_api.extensions import ma, db, dkr, cl


@cl.task(bind=True)
def pathostat_task(self, port):
    total_lines = 35
    total_time = 20 * 60
    pathostat_img = dkr.images.get('pathostat')
    pathostat_run = dkr.containers.run(pathostat_img, detach=True, ports = {3838: port})
    start_time = time.time()
    while (time.time() - start_time < total_time):
        line_count = len(pathostat_run.logs().split('/n'))
        if line_count <= total_lines:
            self.update_state(state='PROGRESS',
                              meta={
                                  'percentage': line_count / total_lines * 100,
                                  'port': port
                              })
        else:
            self.update_state(state='RUNNING',
                              meta={
                                  'time-left': total_time - (time.time() - start_time),
                                  'port': port
                              })
        time.sleep(1)
    pathostat_run.stop()
    return {'time-left': 0, 'status': 'COMPLETED', 'port': port}


class PathoStat(Resource):
    """
        Resource for pathostat
    """
    method_decorators = [jwt_required]

    def get(self):
        port = random.randint(3838, 4000)
        task = pathostat_task.delay(port)
        return {
            "msg": "PathoStat started",
            "task_id": str(task.id)
        }


class PathoStatStatus(Resource):
    """
        Resource for pathostat status query
    """
    method_decorators = [jwt_required]

    def get(self, task_id):
        task = pathostat_task.AsyncResult(task_id)
        if task.state == 'PENDING':
            # job did not start yet
            response = {
                'state': task.state,
                'percentage': 0,
                'status': 'PENDING...',
                'port': task.info.get('port', 'unknown')
            }
        elif task.state == 'PROGRESS':
            response = {
                'state': task.state,
                'percentage': task.info.get('percentage', 0),
                'status': 'LOADING...',
                'port': task.info.get('port', 'unknown')
            }
        elif task.state == 'RUNNING':
            response = {
                'state': task.state,
                'time-left': task.info.get('time-left', 0),
                'status': 'RUNNING...',
                'port': task.info.get('port', 'unknown')
            }
        else:
            response = {
                'state': task.state,
                'status': str(task.info)
            }
        return response
