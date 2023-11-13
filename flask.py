from flask import Flask, render_template, request, jsonify, redirect, url_for
from NetworkManager import scan_wifi, open_wifi, open_ap, get_network_ssid_list, add_network, remove_all_network



app = Flask(__name__)

@app.route('/')
def index():
    try:
        wifi_list = scan_wifi()
        wifi_list = [i for i in wifi_list if r"\x" not in i]
    except:
        wifi_list = []
    return render_template('index.html', items=wifi_list)

@app.route('/submit', methods=['POST'])
def submit():
    ssid = request.form.get('item')
    password = request.form.get('password')
    
    # 密碼長度小於8回傳錯誤
    if len(password) < 8:
        return "0"

    new_network = f"""
network={{
        ssid="{ssid}"
        psk="{password}"
        key_mgmt=WPA-PSK
}}
    """
    
    add_network(new_network)
    return "1"

@app.route('/open_wifi')
def Open_Wifi():
    open_wifi()
    return "opening wifi, this may take few secnods"

@app.route('/remove_all_network')
def Remove_All_Network():
    remove_all_network()
    return redirect(url_for('index'))

if __name__ == '__main__':
    open_ap()
    app.run(host="0.0.0.0",port = 80 , debug=False)
