# py_jdownloader_clicknload_forward_proxy
Emulates a local JDownloader Click'nLoad listener to receive links but forwards them to a LAN instance instead

# Problem
You moved jdownloader into a sandboxed environment (i.e. Docker on your NAS)
The WebBrowser cannot reach local Click'n'Load anymore, browser extensions fail to forward the request and/or generate CORS errors.

# Solution
Provide a minimalistic listener that mimics the Click'N'Load server (without actually decrypting the links) that forwards the request to your docker instance. You can now turn off your workstation and leave the workload to your fileserver.

# vibecoded?
Yes but i needed to test several solutions and debug them so it might worth sharing to save you the hassle.

# TODO (probably won't)
Integrate a neat system try icon
hide the console window

# 🧩 Simple Python CORS Proxy

Ein minimaler HTTP-Proxy-Server in **Python**, der **GET**- und **POST**-Anfragen an einen Zielserver weiterleitet  
und dabei **CORS-Header** (`Access-Control-Allow-*`) automatisch hinzufügt.

Ideal, wenn du im Browser lokal API-Anfragen testen willst, die sonst wegen CORS blockiert würden.

---

## 🚀 Features

- Leitet **GET**- und **POST**-Anfragen an eine Ziel-IP weiter  
- Fügt automatisch **CORS-Header** hinzu  
- Unterstützt **Preflight-Requests (OPTIONS)**  
- Einfache Anpassung der Zieladresse  
- Reines Python — keine externen Webserver nötig

---

## 🧰 Voraussetzungen

- Python ≥ 3.8  
- Modul **requests** (falls nicht vorhanden, installieren mit:)

```bash
pip install requests
