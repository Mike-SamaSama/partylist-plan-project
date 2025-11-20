import functions_framework
from google.cloud import firestore
from datetime import datetime
import json

db = firestore.Client()

@functions_framework.http
def log_submission(request):
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    headers = { 'Access-Control-Allow-Origin': '*' }
    request_json = request.get_json(silent=True)
    
    if request_json and 'docName' in request_json:
        try:
            doc_data = {
                'docName': request_json['docName'],
                'phaseId': request_json['phaseId'],
                'userId': request_json.get('userId', 'anonymous'),
                'timestamp': datetime.now()
            }
            # Write to Firestore
            user_id = doc_data['userId']
            db.collection('party_list_registrations').document(user_id).collection('submissions').add(doc_data)
            
            return (json.dumps({'status': 'success'}), 200, headers)
        except Exception as e:
            return (json.dumps({'error': str(e)}), 500, headers)
            
    return (json.dumps({'error': 'Invalid Data'}), 400, headers)