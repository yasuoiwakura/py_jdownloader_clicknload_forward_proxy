# 🧩 py_jdownloader_clicknload_forward_proxy

A lightweight local **Click’n’Load proxy** for JDownloader that emulates the local listener and forwards requests to a remote (LAN or Docker) JDownloader instance.  
Perfect for setups where your browser and JDownloader no longer share the same host.

---

## 🧠 Problem

You moved JDownloader from your desktop/laptop to a sandboxed environment, for example, a [Docker container using jlesage/docker-jdownloader-2](https://github.com/jlesage/docker-jdownloader-2) on your NAS.
Now your browser extensions can’t reach the local Click’n’Load port anymore, and you start seeing **CORS** or connection errors in your Browser Debugging Network tab.

---

## 💡 Solution

Run this minimalistic Python proxy locally.  
It mimics JDownloader’s Click’n’Load listener and forwards all requests to your LAN or Docker instance instead.  

That way:

- Browser extensions still work  
- You can turn off your workstation  
- The NAS does all the heavy lifting

Works seamlessly with [1] container image

---

## ⚙️ Configuration

Inside the script, you can adjust your target server:

```python
LISTEN_PORT = 9666  # local port to listen on
TARGET_IP = "192.168.0.201"  # JDownloader container or NAS IP
TARGET_PORT = 9666  # usually same as LISTEN_PORT
```

## ❤️ Acknowledgements

- [jlesage] — for making it easy to run JDownloader in Docker
- your fellow AI

## links

[jlesage]: https://github.com/jlesage/docker-jdownloader-2