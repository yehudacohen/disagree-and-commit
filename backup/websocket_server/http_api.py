"""
HTTP REST API for Supervisor Agent and Orchestration Agent
Provides simple HTTP endpoints to call the educational coach system and disagree-and-commit panel
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import asyncio
import logging
from integration.supervisor_client import SupervisorClient
from integration.orchestration_client import OrchestrationClient

logger = logging.getLogger(__name__)


class SupervisorAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Supervisor Agent and Orchestration Agent API"""
    
    supervisor_client = None
    orchestration_client = None
    
    def _set_headers(self, status_code=200, content_type='application/json'):
        """Set response headers"""
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self._set_headers(204)
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/coach':
            self.handle_coach_request()
        elif self.path == '/api/orchestration' or self.path == '/api/panel':
            self.handle_orchestration_request()
        elif self.path == '/api/health':
            self.handle_health_check()
        else:
            self._set_headers(404)
            response = {'error': 'Endpoint not found'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/api/health' or self.path == '/health':
            self.handle_health_check()
        else:
            self._set_headers(404)
            response = {'error': 'Endpoint not found'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def handle_health_check(self):
        """Health check endpoint"""
        self._set_headers(200)
        response = {
            'status': 'healthy',
            'service': 'Educational Coach & Orchestration API',
            'supervisor_available': self.supervisor_client is not None,
            'orchestration_available': self.orchestration_client is not None
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def handle_coach_request(self):
        """Handle educational coach requests"""
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            # Validate required fields
            if 'prompt' not in request_data:
                self._set_headers(400)
                response = {'error': 'Missing required field: prompt'}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            # Extract parameters
            user_input = request_data['prompt']
            session_id = request_data.get('session_id', 'default')
            user_profile = request_data.get('user_profile', {
                'total_xp': 0,
                'level': 1,
                'badges': []
            })
            
            # Call supervisor agent
            if not self.supervisor_client:
                self._set_headers(503)
                response = {'error': 'Supervisor agent not available'}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            # Run async call in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    self.supervisor_client.process_input(
                        user_input=user_input,
                        session_id=session_id,
                        user_profile=user_profile
                    )
                )
            finally:
                loop.close()
            
            # Return response
            self._set_headers(200)
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
            logger.info(f"Processed coach request for session {session_id}")
            
        except json.JSONDecodeError:
            self._set_headers(400)
            response = {'error': 'Invalid JSON in request body'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            logger.error(f"Error processing coach request: {e}")
            self._set_headers(500)
            response = {'error': str(e)}
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def handle_orchestration_request(self):
        """Handle orchestration panel requests"""
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            # Validate required fields
            if 'problem' not in request_data:
                self._set_headers(400)
                response = {'error': 'Missing required field: problem'}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            # Extract parameters
            problem_description = request_data['problem']
            instruction = request_data.get('instruction', None)
            
            # Call orchestration agent
            if not self.orchestration_client:
                self._set_headers(503)
                response = {'error': 'Orchestration agent not available'}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            # Run async call in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    self.orchestration_client.process_problem(
                        problem_description=problem_description,
                        instruction=instruction
                    )
                )
            finally:
                loop.close()
            
            # Return response
            self._set_headers(200)
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
            logger.info(f"Processed orchestration request for problem: {problem_description[:50]}...")
            
        except json.JSONDecodeError:
            self._set_headers(400)
            response = {'error': 'Invalid JSON in request body'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            logger.error(f"Error processing orchestration request: {e}")
            self._set_headers(500)
            response = {'error': str(e)}
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to use our logger"""
        logger.info(f"{self.address_string()} - {format % args}")


def start_http_api_server(host='0.0.0.0', port=8080, supervisor_client=None, orchestration_client=None):
    """
    Start HTTP API server for Supervisor Agent and Orchestration Agent
    
    Args:
        host: Host to bind to
        port: Port to listen on
        supervisor_client: SupervisorClient instance
        orchestration_client: OrchestrationClient instance
    """
    # Set clients as class variables
    SupervisorAPIHandler.supervisor_client = supervisor_client
    SupervisorAPIHandler.orchestration_client = orchestration_client
    
    # Create server
    server = HTTPServer((host, port), SupervisorAPIHandler)
    
    logger.info(f"HTTP API server started at http://{host}:{port}")
    logger.info(f"Endpoints:")
    logger.info(f"  POST http://{host}:{port}/api/coach - Call educational coach")
    logger.info(f"  POST http://{host}:{port}/api/orchestration - Call disagree-and-commit panel")
    logger.info(f"  POST http://{host}:{port}/api/panel - Call disagree-and-commit panel (alias)")
    logger.info(f"  GET  http://{host}:{port}/api/health - Health check")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("HTTP API server stopped")
        server.shutdown()


if __name__ == "__main__":
    # For testing
    import os
    logging.basicConfig(level=logging.INFO)
    
    # Initialize clients
    supervisor_client = SupervisorClient()
    orchestration_client = OrchestrationClient()
    
    # Start server
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8080"))
    
    start_http_api_server(host, port, supervisor_client, orchestration_client)
