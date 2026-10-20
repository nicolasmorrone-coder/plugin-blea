from http.server import HTTPServer,BaseHTTPRequestHandler
import threading,subprocess,time,socket,os,tempfile
class H(BaseHTTPRequestHandler):
 def do_GET(self):self.send_response(200);self.end_headers();self.wfile.write(b'OK')
 def do_POST(self):self.rfile.read(int(self.headers.get('Content-Length','0')));self.do_GET()
 def log_message(self,*a):pass
server=HTTPServer(('127.0.0.1',18994),H);threading.Thread(target=server.serve_forever,daemon=True).start()
base=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources')
for cycle in range(3):
 pid='/tmp/suite4-blea-'+str(cycle)+'.pid'
 with open('/tmp/suite4-blea-'+str(cycle)+'.log','w') as log:
  p=subprocess.Popen([base+'/python_venv/bin/python3',base+'/blead/blead.py','--device','hci0','--socketport','18996','--sockethost','127.0.0.1','--callback','http://127.0.0.1:18994/','--apikey','synthetic','--pid',pid,'--daemonname','suite4','--loglevel','debug'],stdout=log,stderr=log)
  try:
   for i in range(100):
    if p.poll() is not None:raise RuntimeError('BLEA stopped before opening socket; see cycle log')
    try:
     with socket.create_connection(('127.0.0.1',18996),timeout=.1):break
    except OSError:time.sleep(.1)
   else:raise RuntimeError('No BLEA socket')
   print('BLEA_SOCKET_START_PASS',cycle,flush=True)
  finally:
   p.terminate()
   try:p.wait(timeout=10)
   except subprocess.TimeoutExpired:p.kill();p.wait();raise
  assert p.returncode==0,p.returncode
  assert not os.path.exists(pid),pid
  print('BLEA_SIGTERM_CLEAN_STOP_PASS',cycle,flush=True)
server.shutdown();server.server_close()
print('NO_BLUETOOTH_RADIO_VALIDATION')
