from miniagent import app, configure

port=configure.get('PORT') or 5000

app.run(host="0.0.0.0", port=port, use_reloader=False, debug=True)