import functions_framework
from google.cloud import firestore
from datetime import datetime
import json

# Initialize Firestore
db = firestore.Client()

@functions_framework.http
def log_submission(request):
    # 1. Handle CORS (Cross-Origin Resource Sharing)
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    # 2. Parse the data sent from your HTML website
    request_json = request.get_json(silent=True)
    
    # CORRECTION 1: Verify 'phaseId' is present to prevent errors
    if request_json and 'docName' in request_json and 'phaseId' in request_json:
        try:
            # 3. Prepare the data packet
            doc_data = {
                'docName': request_json['docName'],
                'phaseId': request_json['phaseId'],
                'userId': request_json.get('userId', 'anonymous'),
                'timestamp': datetime.now(),
                # CORRECTION 2: Add source tag to track Cloud Run usage
                'source': 'web_app_tracker_cloud_run'
            }
            
            # 4. Write to Google Firestore Database
            user_id = doc_data['userId']
            db.collection('party_list_registrations').document(user_id).collection('submissions').add(doc_data)
            
            # CORRECTION 3: Return a specific confirmation message
            return (json.dumps({'status': 'success', 'message': f"Logged: {doc_data['docName']}"}), 200, headers)
            
        except Exception as e:
            return (json.dumps({'status': 'error', 'message': str(e)}), 500, headers)
            
    return (json.dumps({'status': 'error', 'message': 'Invalid Data'}), 400, headers)