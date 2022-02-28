# -*- coding: utf-8 -*-
import string
import zipfile
import os
# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
# 代理隧道验证信息 使用自己的
proxyUser = "H8S586W474G3FFFF"
proxyPass = "F516EB811111"


def create_proxy_auth_extension(proxy_host, proxy_port, proxy_username, proxy_password, scheme='http', plugin_path=None):
    if plugin_path is None:
        plugin_path = os.getcwd() + rf'/{proxy_username}_{proxy_password}@http-dyn.abuyun.com_9020.zip'

    manifest_json = """
       {
           "version": "1.0.0",
           "manifest_version": 2,
           "name": "Abuyun Proxy",
           "permissions": [
               "proxy",
               "tabs",
               "unlimitedStorage",
               "storage",
               "<all_urls>",
               "webRequest",
               "webRequestBlocking"
           ],
           "background": {
               "scripts": ["background.js"]
           },
           "minimum_chrome_version":"22.0.0"
       }
       """

    background_js = string.Template(
        """
        var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                },
                bypassList: ["foobar.com"]
            }
          };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
        );
        """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )

    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return plugin_path


# 创建插件代理,如果文件已经创建,就不必再创建了
proxy_auth_plugin_path = create_proxy_auth_extension(proxy_host=proxyHost, proxy_port=proxyPort, proxy_username=proxyUser, proxy_password=proxyPass)
print("cccccccc")
